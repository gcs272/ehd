#!/usr/bin/env python

from flask import Flask, redirect, url_for, session, request, g,\
        render_template

import stripe
import json
import uuid
import os

main = Flask(__name__)
main.config.from_pyfile('config/development.cfg')

from etsy import etsy
main.register_blueprint(etsy, url_prefix='/etsy')

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/create')
def create_postcard():
	return render_template('create_postcard.html')

@main.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        if 'stripeToken' in request.form:
            amount = int(session.get('number_of_cards', 1)) * 150

            print 'Got token: %s' % (request.form.get('stripeToken'))
            stripe.api_key = main.config['STRIPE_SECRET_KEY']
            token = request.form.get('stripeToken')
            charge = stripe.Charge.create(
                amount = amount,
                currency = 'usd',
                card=token,
                description=session.get('user-email'))
            return redirect(url_for('hooray'))

    return render_template('checkout.html')

@main.route('/image/generate', methods=['POST'])
def generate():
    # Grab the list of urls being posted and start downloading them
    card = Postcard()
    for url in json.loads(request.form.get('images')):
        card.add_image(download_image(url))

    grid_x = int(request.form.get('grid_x'))
    grid_y = int(request.form.get('grid_y'))

    card.generate_grid((grid_x, grid_y))

    path = download_image(request.form.get('banner'))
    card.place_banner(path, 'twothirds')

    id = str(uuid.uuid4())
    outpath = '/tmp/%s.jpg' % (id)
    canvas.quarter().save(outpath)
    return jsonify({'preview': url_for('preview', id=id)})

@main.route('/image/preview')
def preview():
    path = '/tmp/%s.jpg' % (request.args.get('id'))
    response = make_response(open(path).read())
    response.headers['Content-Type'] = 'image/jpeg'
    response.headers['Content-Disposition'] = 'attachment; filename=img.jpg'
    return response

@main.route('/hooray')
def hooray():
    return render_template('hooray.html')

def download_image(url):
    path = '/tmp/%s.jpg' % (hashlib.sha1(url).hexdigest())
    if os.path.exists(path):
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
