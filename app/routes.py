from sched import scheduler

from flask import Blueprint, render_template, request, redirect, url_for
from .models import db, Game, Price

main = Blueprint("main", __name__)

@main.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        game = Game(name=name, platform="steam")
        db.session.add(game)
        db.session.commit()
        return redirect(url_for("main.index"))

    games = Game.query.all()
    return render_template("index.html", games=games)

@main.route("/game/<int:game_id>")
def game_detail(game_id):
    game = Game.query.get_or_404(game_id)
    prices = Price.query.filter_by(game_id=game.id).order_by(Price.date).all()

    # Pretvori SQLAlchemy objekte u dict (JSON-serializable)
    prices_data = [
        {
            'date': price.date.strftime('%Y-%m-%d'),
            'price': price.price
        }
        for price in prices
    ]

    return render_template("game_detail.html", game=game, prices=prices_data)

