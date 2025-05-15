# app/scraper/scraper.py
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from app.models import db, Game, Price  # Uvozimo modele za bazu
import time

def get_steam_price(game_name):
    query = game_name.replace(' ', '+')
    search_url = f"https://store.steampowered.com/search/?term={query}"

    options = Options()
    options.add_argument('--headless')
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(search_url)
        time.sleep(2)
        first_result = driver.find_element("css selector", ".search_result_row")
        first_result.click()
        time.sleep(3)

        try:
            price = driver.find_element("class name", "discount_final_price").text
        except:
            price = driver.find_element("class name", "game_purchase_price").text

        price = float(price.replace("€", "").replace(",", ".").strip())  # Pretvori cenu u float
        print(f"Cena za igru '{game_name}' je {price} EUR.")

        # Proveri da li igra postoji u bazi
        game = Game.query.filter_by(name=game_name).first()

        if not game:
            # Ako igra ne postoji u bazi, dodaj je
            game = Game(name=game_name, platform="steam")
            db.session.add(game)
            db.session.commit()

        # Upisivanje cene u bazu
        new_price = Price(price=price, game_id=game.id)
        db.session.add(new_price)
        db.session.commit()
        return price

    except Exception as e:
        print("Greška u scraping-u:", e)
        return None

    finally:
        driver.quit()
