from datetime import datetime
from app.models import Game, Price, db
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException


def get_gog_price(game_name: str) -> str:
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        search_url = f"https://www.gog.com/en/games?query={game_name}"
        driver.get(search_url)

        wait = WebDriverWait(driver, 15)

        # Pokušaj da klikneš na cookie prihvatanje
        try:
            cookie_btn = wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
            cookie_btn.click()
        except TimeoutException:
            pass

        # Ukloni eventualne preostale cookie elemente koji blokiraju klik
        try:
            driver.execute_script("""
                let ids = ['CybotCookiebotDialog', 'CybotCookiebotDialogBodyContentTitle', 'CybotCookiebotDialogBodyContentText'];
                ids.forEach(id => {
                    let el = document.getElementById(id);
                    if (el) el.remove();
                });
            """)
        except Exception as e:
            print("Greška prilikom uklanjanja cookie elemenata:", e)

        # Sačekaj da se rezultati pojave
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.product-tile")))

        # Klikni na prvi rezultat pomoću JavaScript-a (sigurnije u headless režimu)
        first_result = driver.find_element(By.CSS_SELECTOR, "a.product-tile")
        driver.execute_script("arguments[0].click();", first_result)

        # Sačekaj da se stranica igre učita i cena pojavi
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.product-actions-price__final-amount")))
        price = driver.find_element(By.CSS_SELECTOR, "span.product-actions-price__final-amount").text

        return price

    except (TimeoutException, NoSuchElementException) as e:
        print(f"[GOG SCRAPER ERROR] {game_name}: {e}")
        return "N/A"

    finally:
        driver.quit()

def scrape_all_games():
    print("Scraping all games started")  # Dodaj ovaj print
    games = Game.query.all()
    for game in games:
        price = get_gog_price(game.name)
        if price is not None:
            new_price = Price(game_id=game.id, price=price, date=datetime.utcnow())
            db.session.add(new_price)
            print(f"[SCRAPED] {game.name} – {price} €")
    db.session.commit()

