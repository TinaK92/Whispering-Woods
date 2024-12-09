from app.models import db, Listing, environment, SCHEMA
from sqlalchemy.sql import text


def undo_listings():
    if environment == 'production':
        db.session.execute(f"TRUNCATE table {SCHEMA}.listings RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM listings"))

    db.session.commit()