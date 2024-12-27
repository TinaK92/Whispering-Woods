from app.models import db, Size, environment, SCHEMA
from sqlalchemy.sql import text

def seed_sizes():
    sizes = [
        {"name": "XS"},
        {"name": "S"},
        {"name": "M"},
        {"name": "L"},
        {"name": "XL"},
        {"name": "2XL"},
        {"name": "3XL"},
        {"name": "4XL"},
        {"name": "5XL"},
    ]

    for size_data in sizes:
        size = Size.query.filter_by(name=size_data["name"]).first()
        if not size:  # Prevent duplicates
            size = Size(**size_data)
            db.session.add(size)
    db.session.commit()

def undo_seed_sizes():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.sizes RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM sizes;"))
        
    db.session.commit()