#!/usr/bin/env python

from flask import Flask, redirect, url_for, session, request, g,\
        render_template
import stripe

main = Flask(__name__)
main.config.from_pyfile('config/development.cfg')

from etsy import etsy
main.register_blueprint(etsy, url_prefix='/etsy')

@main.route('/')
def index():
    return render_template('index.html')

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

@main.route('/hooray')
def hooray():
    return render_template('hooray.html')
