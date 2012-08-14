from flask import Blueprint, g, url_for, redirect, session, request, flash, render_template, jsonify
from flaskext.oauth import OAuth
from app import main
import random

etsy = Blueprint('etsy', __name__)

oauth = OAuth()
api = oauth.remote_app('etsy',
    base_url = main.config['ETSY_BASE_URL'],
    request_token_url= main.config['ETSY_REQUEST_TOKEN_URL'],
    access_token_url= main.config['ETSY_ACCESS_TOKEN_URL'],
    authorize_url= main.config['ETSY_AUTHORIZE_URL'],
    consumer_key= main.config['ETSY_CONSUMER_KEY'],
    consumer_secret= main.config['ETSY_CONSUMER_SECRET'],
    request_token_params=dict(scope= main.config['ETSY_SCOPE'], limit=main.config['ETSY_API_LIMIT'])
)

### routes ###
@etsy.route('/')
def index():
    access_token = get_token();
    if access_token is None:
        return redirect(url_for('etsy.register'))

    return redirect(url_for('create_postcard'))

### auth routes ###
@etsy.route('/register')
def register():
    return api.authorize(callback=url_for('etsy.verify', next=request.args.get('next') or request.referrer or None))

@etsy.route('/verify')
@api.authorized_handler
def verify(resp):

    next_url = request.args.get('next') or url_for('etsy.index')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)

    session['etsy_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )

    flash(u'You were signed in!')
    return redirect(next_url)

### Wrapper for OAuth get method, validates response.
def get(uri):
    resp = api.get(uri)
    if resp.status == 200:
        data = resp.data
    else:
        data = None
        
    return data

### api routes ###

# Return the current or given user
def get_user(id="__SELF__"):
    return get('http://openapi.etsy.com/v2/users/'+id+'/')

# Return all transactions for the current or given user
def get_transactions(userid="__SELF__"):
    return get('http://openapi.etsy.com/v2/users/'+userid+'/transactions/')

# Return a specific transaction for the current or given user
def get_transaction(userid="__SELF__", transactionid=None):
    if transactionid is None: return None
    return get('http://openapi.etsy.com/v2/users/'+userid+'/transactions/' + transactionid)

# Return all shops for the current or given user
def get_shops(userid="__SELF__"):
    return get('http://openapi.etsy.com/v2/users/'+userid+'/shops/')

# Return a specific shop for the current or given user
def get_shop(userid="__SELF__", shopid=None):
    if shopid is None: return None
    return get('http://openapi.etsy.com/v2/users/'+userid+'/shops/' + shopid)

# Return the User's avatar URL
def get_avatar(userid="__SELF__"):
    return get('http://openapi.etsy.com/v2/users/'+str(userid)+'/avatar/src')

# Return active listings for a shop
def get_shop_listings(shopid=None):
    if shopid is None: return None
    return get('http://openapi.etsy.com/v2/shops/'+str(shopid)+'/listings/active')

# Return a specific image for a specific listing
def get_listing_image(listingid=None, imageid=None):
    if listingid is None or imageid is None: return None
    return get('http://openapi.etsy.com/v2/listings/'+str(listingid)+'/images/' + imageid)

# Return all images for a listing
def get_listing_images(listingid=None):
    if listingid is None: return None
    return get('http://openapi.etsy.com/v2/listings/'+str(listingid)+'/images')

### Specifc routes for EHD
@etsy.route('/customers')
def get_customers():
    return jsonify(get_shop_receipts())

@etsy.route('/images')
def get_images():
    return jsonify(get_shop_images())

@etsy.route('/store')
def test():
    shop_data = get_all_receipts()
    return render_template('etsy/shops.html', stores=shop_data)

# Get all receipts for a the current user's shop and return customer information.
def get_all_receipts():
    shops = get_shops()

    i = 0
    numShops = shops.get('count')

    shopList = dict()

    for i in range(0, numShops):
        s = shops['results'][i]
        shop_name = s.get('shop_name')
        shop_id = s.get('shop_id')
        owner_id = s.get('user_id')
        owner_login = s.get('login_name')
        shop_receipts = get_receipts_for_shop(shop_id)
        numReceipts = shop_receipts.get('count')

        shop_customers = {}

        for j in range(0, numReceipts):
            sr =  shop_receipts['results'][j];
            customer_id = sr.get('buyer_user_id')
            if customer_id in shop_customers:
                shop_customers[customer_id]['sum'] += float(sr.get('total_price'))
                shop_customers[customer_id]['num_orders'] += 1
            else:
                shop_customers[customer_id] = dict()
                shop_customers[customer_id]['name'] = sr.get('name')
                shop_customers[customer_id]['email'] = sr.get('email')

                shop_customers[customer_id]['address'] = dict()
                shop_customers[customer_id]['address']['first_line'] = sr.get('first_line')
                shop_customers[customer_id]['address']['second_line'] = sr.get('second_line')
                shop_customers[customer_id]['address']['city'] = sr.get('city')
                shop_customers[customer_id]['address']['state'] = sr.get('state')
                shop_customers[customer_id]['address']['zip'] = sr.get('zip')
                shop_customers[customer_id]['address']['country'] = sr.get('country_id')

                shop_customers[customer_id]['sum'] = float(sr.get('total_price'))
                shop_customers[customer_id]['num_orders'] = 1

        shopList[shop_id] = dict()
        shopList[shop_id]['shop_name'] = shop_name
        shopList[shop_id]['shop_id'] = shop_id
        shopList[shop_id]['owner_id'] = owner_id
        shopList[shop_id]['owner_login'] = owner_login
        shopList[shop_id]['shop_customers'] = shop_customers

    return shopList

# Returns a shops receipts for the given shop
def get_receipts_for_shop(shopid=None):
    if shopid is None: return None

    resp = api.get('http://openapi.etsy.com/v2/shops/'+str(shopid)+'/receipts/')

    if resp.status == 200:
        data = resp.data
    else:
        data = None
        
    return data

# Returns a shops images, banner and user avatar.
def get_shop_images(shopid=None):
    if shopid == None:
        shop_data = get_shops(userid="__SELF__")['results'][0]
    else:
        shop_data = get_shop(userid="__SELF__", shopid=shopid)['results'][0]

    results = dict()
    results['banner'] = shop_data['image_url_760x100'];
    results['avatar'] = get_avatar()['results']['src'];
    results['images'] = []
    listings = get_shop_listings(shop_data['shop_id'])
    numListings = listings['count']
    listings = listings['results']

    urls = []
    for listing in listings:
        images = get_listing_images(listing['listing_id'])
        for image in images['results']:
            urls.append(image['url_fullxfull'])

    results['images'] = urls
    return results

### utility routes ###
@api.tokengetter
def get_token():
    return session.get('etsy_token')
