from app.models import db, listing_size, environment, SCHEMA
from sqlalchemy.sql import text


# Seed function
def seed_listing_sizes():
    if environment == "production":
        # In production, add schema support
        db.session.execute(f"SET search_path TO {SCHEMA}")

    # Add your seed data here if needed in the future
    # Example:
    # listing_size1 = ListingSize(listing_id=1, size_id=1)
    # db.session.add(listing_size1)

    db.session.commit()


# Undo function to truncate the table
def undo_listing_sizes():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.listing_sizes RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM listing_sizes"))
        
    db.session.commit()