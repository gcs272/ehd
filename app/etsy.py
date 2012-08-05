from flask import Blueprint, g, url_for, redirect, session, request, flash
from flaskext.oauth import OAuth

from app import main

etsy = Blueprint('etsy', __name__)

oauth = OAuth()
api = oauth.remote_app('etsy',
    base_url = main.config['ETSY_BASE_URL'],
    request_token_url= main.config['ETSY_REQUEST_TOKEN_URL'],
    access_token_url= main.config['ETSY_ACCESS_TOKEN_URL'],
    authorize_url= main.config['ETSY_AUTHORIZE_URL'],
    consumer_key= main.config['ETSY_CONSUMER_KEY'],
    consumer_secret= main.config['ETSY_CONSUMER_SECRET'],
    request_token_params=main.config['ETSY_SCOPE']
)



### routes ###
@etsy.route('/')
def index():
    access_token = get_token();
    if access_token is None:
        return redirect(url_for('etsy.register'))

    return "%s %s" % access_token

### auth routes ###
@etsy.route('/register')
def register():
    print url_for('etsy.verify')
    return api.authorize(callback=url_for('etsy.verify', next=request.args.get('next') or request.referrer or None))

@etsy.route('/verify')
@api.authorized_handler
def verify(resp):
    print resp
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

### api routes ###
@etsy.route('/users/')
@etsy.route('/users/<id>')
def get_user(id=None):
    if id is None:
        id = "__SELF__"

    resp = api.get('http://openapi.etsy.com/v2/users/'+id+'/')

    if resp.status == 200:
        data = resp.data
    else:
        data = None
        
    return str(data)

@etsy.route('/users/<userid>/transactions/')
def get_transactions(userid=None):
    if userid is None:
        userid = "__SELF__"

    resp = api.get('http://openapi.etsy.com/v2/users/'+userid+'/transactions/')
    print resp.data
    if resp.status == 200:
        data = resp.data
    else:
        data = None
        
    return str(data)

@etsy.route('/users/<userid>/transactions/<transactionid>')
def get_transaction(userid=None, transactionid=None):
    if userid is None:
        userid = "__SELF__"

    if transactionid is None:
        return get_transactions(userid)

    resp = api.get('http://openapi.etsy.com/v2/users/'+userid+'/transactions/' + transactionid)

    if resp.status == 200:
        data = resp.data
    else:
        data = None
        
    return str(data)

@etsy.route('/users/<userid>/shops/')
def get_shops(userid=None):
    if userid is None:
        userid = "__SELF__"

    resp = api.get('http://openapi.etsy.com/v2/users/'+userid+'/shops/')
    print resp.data
    if resp.status == 200:
        data = resp.data
    else:
        data = None
        
    return str(data)

@etsy.route('/users/<userid>/shops/<shopid>')
def get_shop(userid=None, shopid=None):
    if userid is None:
        userid = "__SELF__"

    if shopid is None:
        return get_shops(userid)

    resp = api.get('http://openapi.etsy.com/v2/users/'+userid+'/shops/' + shopid)

    if resp.status == 200:
        data = resp.data
    else:
        data = None
        
    return str(data)

### utility routes ###
@api.tokengetter
def get_token():
    return session.get('etsy_token')
