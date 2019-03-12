import os
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)

basedir ='/var/www/book-s/book-store-tutorial-flask/'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////var/www/book-s/book-store-tutorial-flask/database.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(basedir, 'database.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
