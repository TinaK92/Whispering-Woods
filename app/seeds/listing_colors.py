from app.models import db, listing_color, environment, SCHEMA
from sqlalchemy.sql import text


# Seed function
def seed_listing_colors():
    if environment == "production":
        # In production, add schema support
        db.session.execute(f"SET search_path TO {SCHEMA}")

    # Add your seed data here if needed in the future
    # Example:
    # listing_color1 = ListingColor(listing_id=1, color_id=1)
    # db.session.add(listing_color1)

    db.session.commit()


# Undo function to truncate the table
def undo_listing_colors():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.listing_colors RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM listing_colors"))
        
    db.session.commit()