import os

from flask import Flask
from .models import db
from .routes import main  # Blueprint

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")  # ili tvoja putanja
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    app.register_blueprint(main)

    return app
