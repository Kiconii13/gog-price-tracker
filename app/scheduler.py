from app.models import Game, Price, db
from app.scraper.steam_scraper import get_steam_price
from datetime import date

def update_prices(app):
    with app.app_context():
        games = Game.query.all()
        for game in games:
            if game.platform == "steam":
                price = get_steam_price(game.name)
                if price:
                    existing = Price.query.filter_by(game_id=game.id, date=date.today()).first()
                    if not existing:
                        db.session.add(Price(game_id=game.id, price=price))
                        db.session.commit()

from apscheduler.schedulers.background import BackgroundScheduler

def start_scheduler(app):
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=lambda: update_prices(app), trigger="interval", hours=24)
    scheduler.start()
