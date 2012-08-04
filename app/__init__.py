#!/usr/bin/env python

from flask import Flask, redirect, url_for, session, request, g
from flaskext.oauth import OAuth
import urllib

SECRET_KEY = 'H4ckD4y'
DEBUG = True

main = Flask(__name__)
main.config.from_pyfile('config/development.cfg')

### ETSY Constants ###
ETSY_SCOPE = "transactions_r"
ETSY_CALLBACK = 'http://localhost/verify'
####

oauth = OAuth()
api = oauth.remote_app('etsy',
    base_url='http://openapi.etsy.com/v2',
    request_token_url='http://openapi.etsy.com/v2/oauth/request_token',
    access_token_url='http://openapi.etsy.com/v2/oauth/access_token',
    authorize_url='https://www.etsy.com/oauth/signin',
    consumer_key="02wmxtqp2h",
    consumer_secret="5g97shoangs67rtrcn4cqmsi"
)

### routes ###
@main.route('/')
def index():
    access_token = get_token();
    if access_token is None:
        return redirect(url_for('register'))

    return "%s %s" % access_token

@main.route('/register')
def register():
    return api.authorize(callback=url_for('verify',
        next=request.args.get('next') or request.referrer or None))

@main.route('/verify')
@api.authorized_handler
def verify(resp):
    next_url = request.args.get('next') or url_for('index')
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
