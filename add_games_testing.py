from flask import Flask
from app.models import Game, db


def add_games():
    # Define the games to add
    games = [
        {"name": "Game 1", "platform": "steam"},
        {"name": "Game 2", "platform": "steam"},
        {"name": "Game 3", "platform": "steam"},
    ]

    app = Flask(__name__, template_folder='app/templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    db.init_app(app)

    # Use the app context to interact with the database
    with app.app_context():
        for game_data in games:
            game = Game(name=game_data["name"], platform=game_data["platform"])
            db.session.add(game)
        db.session.commit()


if __name__ == "__main__":
    add_games()
