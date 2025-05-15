from app import create_app
from app.models import db, Price
from sqlalchemy import func

app = create_app()

with app.app_context():
    # 1. Pronađi sve unikatne kombinacije game_id i date
    unique_entries = db.session.query(
        Price.game_id,
        func.date(Price.date).label('date')
    ).group_by(
        Price.game_id,
        func.date(Price.date)
    ).all()

    total_deleted = 0

    for game_id, date in unique_entries:
        # Pronađi sve unose za taj game_id i taj dan
        all_prices = Price.query.filter(
            Price.game_id == game_id,
            func.date(Price.date) == date
        ).order_by(Price.date.desc()).all()

        # Zadrži samo prvi (najnoviji), ostale obriši
        if len(all_prices) > 1:
            to_delete = all_prices[1:]  # sve osim prvog
            for price in to_delete:
                db.session.delete(price)
                total_deleted += 1

    db.session.commit()
    print(f"Obrisano duplikata: {total_deleted}")
