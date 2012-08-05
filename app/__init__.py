#!/usr/bin/env python

from flask import Flask, redirect, url_for, session, request, g,\
        render_template

main = Flask(__name__)
main.config.from_pyfile('config/development.cfg')

from etsy import etsy
main.register_blueprint(etsy, url_prefix='/etsy')

@main.route('/')
def index():
    return render_template('index.html')
