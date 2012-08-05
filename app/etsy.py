from flask import Blueprint, g, url_for, redirect, session, request
from flaskext.oauth import OAuth
import urllib

from app import main

etsy = Blueprint('etsy', __name__)

oauth = OAuth()
api = oauth.remote_app('etsy',
    base_url = main.config['ETSY_BASE_URL'],
    request_token_url= main.config['ETSY_REQUEST_TOKEN_URL'],
    access_token_url= main.config['ETSY_ACCESS_TOKEN_URL'],
    authorize_url= main.config['ETSY_AUTHORIZE_URL'],
    consumer_key= main.config['ETSY_CONSUMER_KEY'],
    consumer_secret= main.config['ETSY_CONSUMER_SECRET']
)

### routes ###
@etsy.route('/')
def index():
    access_token = get_token();
    if access_token is None:
        return redirect(url_for('etsy.register'))

    return "%s %s" % access_token

@etsy.route('/register')
def register():
    return api.authorize(callback=url_for('etsy.verify',
        next=request.args.get('next') or request.referrer or None))

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

### utilities ###
@api.tokengetter
def get_token():
    return session.get('etsy_token')
