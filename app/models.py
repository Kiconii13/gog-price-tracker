from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    platform = db.Column(db.String(50), nullable=False)  # npr. steam

class Price(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow)
    price = db.Column(db.Float, nullable=False)
