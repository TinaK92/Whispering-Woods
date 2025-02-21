from app.models import db, image_color, environment, SCHEMA
from sqlalchemy.sql import text


# Seed function
def seed_image_colors():
    if environment == "production":
        # In production, add schema support
        db.session.execute(f"SET search_path TO {SCHEMA}")

    # Add your seed data here if needed in the future
    # Example:
    # image_color1 = ImageColor(
    #     image_id=1,
    #     color_id=1,
    # )
    # db.session.add(image_color1)

    db.session.commit()


# Undo function to truncate the table
def undo_image_colors():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.image_colors RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM image_colors"))
        
    db.session.commit()