from app import create_app
from app.scraper.gog_scraper import scrape_all_games

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        scrape_all_games()
