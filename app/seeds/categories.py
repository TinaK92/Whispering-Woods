from app.models import db, Category, environment, SCHEMA
from sqlalchemy.sql import text


def seed_categories():
    categories = [
        "Reptile",
        "Exotic",
        "Livestock",
        "Domesticated",
    ]

    for name in categories:
        category = Category(name=name)
        db.session.add(category)

    db.session.commit()


def undo_categories():
    if environment == "production":
        db.session.execute(
            f"TRUNCATE table {SCHEMA}.categories RESTART IDENTITY CASCADE;"
        )
    else:
        db.session.execute(text("DELETE FROM categories"))

    db.session.commit()
