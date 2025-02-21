from app.models import db, Image, environment, SCHEMA
from sqlalchemy.sql import text


# Seed function
def seed_images():
    if environment == "production":
        # In production, add schema support
        db.session.execute(f"SET search_path TO {SCHEMA}")

    # Add your seed data here if needed in the future
    # Example:
    # image1 = Image(
    #     listing_id=1,
    #     color_id=1,
    #     front_image_url="https://example.com/front_image.jpg",
    #     back_image_url="https://example.com/back_image.jpg"
    # )
    # db.session.add(image1)

    db.session.commit()


# Undo function to truncate the table
def undo_images():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.images RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM images"))
        
    db.session.commit()