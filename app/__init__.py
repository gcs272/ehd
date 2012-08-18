#!/usr/bin/env python

from flask import Flask, redirect, url_for, session, request, g,\
        render_template, jsonify, make_response, flash

from lib.postcard import Postcard

import requests
import stripe
import json
import uuid
import os
import hashlib

main = Flask(__name__)
main.config.from_pyfile('config/development.cfg')

from etsy import etsy
main.register_blueprint(etsy, url_prefix='/etsy')

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/create')
def create_postcard():
    if session.get('etsy_token') is not None:
        return render_template('create_postcard.html')
    else:
        ## redirect to sorry page? verify again?
        flash(u'Sorry! We were unable to connect to Etsy, please try again!');
        return redirect(url_for('index'));

@main.route('/recipients')
def add_recipients():
    if session.get('card_id') is not None:
        return render_template('recipients.html')
    else:
        return card_required()

@main.route('/checkout', methods=['POST'])
def checkout_form():
    addresses = json.loads(request.form.get('addresses'))
    message = request.form.get('message')

    return render_template('checkout.html', addresses=addresses, 
            message=message, total_cost = 1.99 * len(addresses))

@main.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if session.get('card_id') is None:
        return card_required()

    if request.method == 'POST':
        if 'stripeToken' in request.form:
            amount = int(session.get('number_of_cards', 1)) * 150

            stripe.api_key = main.config['STRIPE_SECRET_KEY']
            token = request.form.get('stripeToken')
            charge = stripe.Charge.create(
                amount = amount,
                currency = 'usd',
                card=token,
                description=session.get('user-email'))

            ## change later, if we're storing transaction info or something..
            session['transaction_id'] = 1337

            return redirect(url_for('hooray'))
    #detect if they've generated a card and transaction?
    return render_template('checkout.html')

@main.route('/image/generate', methods=['POST'])
def generate():
    # Grab the list of urls being posted and start downloading them
    card = Postcard()
    grid_x = int(request.form.get('layout_x'))
    grid_y = int(request.form.get('layout_y'))
    
    # Set the background color
    card.set_background(request.form.get('background'))
   
    urls = json.loads(request.form.get('images'))
    # DEBUG: add junk data to fill up a 3x3 grid
    urls += urls
    urls += urls
    
    # Shorten to just what we actually need
    urls = urls[0:grid_x*grid_y]

    for url in urls:
        card.add_image(download_image(url))

    card.generate_grid((grid_x, grid_y))

    banner = json.loads(request.form.get('banner'))
    if banner['showBanner']:
        path = download_image(banner['src'])
        card.place_banner(path, banner['placement'])

    id = str(uuid.uuid4())
    outpath = '/tmp/%s.jpg' % (id)
    card.canvas.save(outpath)
    session['card_path'] = outpath
    session['card_id'] = id

    preview_path = '/tmp/%s-preview.jpg' % (id)
    card.quarter().save(preview_path)
    return jsonify({'preview': url_for('preview', id=id)})

@main.route('/image/preview')
def preview():
    path = '/tmp/%s-preview.jpg' % (request.args.get('id'))
    response = make_response(open(path).read())
    response.headers['Content-Type'] = 'image/jpeg'
    return response

@main.route('/hooray', methods=['POST'])
def hooray():
    if session.get('card_id') is None:
        return card_required();

    if session.get('transaction_id') is None:
        flash(u'Whoops! Looks like you forgot to checkout.')
        return redirect(url_for('checkout'))
    ## Should we clear the postcard info from session?
    return render_template('hooray.html')

def download_image(url):
    path = '/tmp/%s.jpg' % (hashlib.sha1(url).hexdigest())
    if not os.path.exists(path):
        res = requests.get(url)
        fp = open(path, 'wb')
        fp.write(res.content)
        fp.close()

    return path

def get_session(id):
    path = '/tmp/%s.json' % (id)
    return json.loads(open(path).read())

def put_session(id, data):
    fp = open('/tmp/%s.json' % (id), 'wb')
    fp.write(json.dumps(data))
    fp.close()

def card_required():
    flash(u"Try generating a card first!")
    return redirect(url_for('create_postcard'))
