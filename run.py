# run.py ili glavni fajl za pokretanje

from app import create_app

# Kreiraj aplikaciju
app = create_app()

# Pokreni aplikaciju unutar konteksta
if __name__ == "__main__":
    with app.app_context():  # Osiguraj aplikacijski kontekst
        app.run(debug=True)
