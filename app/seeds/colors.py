from app.models import db, Color, Listing, environment, SCHEMA
from sqlalchemy.sql import text

def seed_colors():
    
    colors = [
        {"name": "Dark Heather Grey"},
        {"name": "Ice Blue"},
        {"name": "Heather Light Pink"},
        {"name": "Heather Forest Green"},
        {"name": "Charcoal"},
        {"name": "Sport Grey"},
        {"name": "Light Blue"},
        {"name": "Light Pink"},
        {"name": "Sand"},
        {"name": "Stone Blue"},
        {"name": "Military Green"},
        {"name": "White"},
        {"name": "Black"},
        {"name": "Navy"},
        {"name": "Carolina Blue"},
        {"name": "Irish Green"},
        {"name": "Purple"},
        {"name": "Red"},
        {"name": "Daisy"},
    ]

    for data in colors:
        color = Color(
            name=data["name"]
        )
        db.session.add(color)

    db.session.commit()

def undo_seed_colors():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.colors RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM colors;"))
        
    db.session.commit()
