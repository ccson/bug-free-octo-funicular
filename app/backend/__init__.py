from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from . import config


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_CONNECTION_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()
db = SQLAlchemy(app)

