
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from flask_bcrypt import Bcrypt

app = Flask(__name__)

# the toolbar is only enabled in debug mode:
app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = 'ff749f4574abef07a564b2d1'


db = SQLAlchemy(app)
toolbar = DebugToolbarExtension(app)
bcrypt = Bcrypt(app)

from market import routes