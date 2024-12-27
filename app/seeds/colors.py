from app.models import db, Color, environment, SCHEMA
from sqlalchemy.sql import text


def seed_colors():
    colors = [
        {
            "name": "Dark Heather Grey",
            "front_image_url": "url_to_front_dark_heather_grey",
            "back_image_url": "url_to_back_dark_heather_grey",
        },
        {
            "name": "Ice Blue",
            "front_image_url": "url_to_front_ice_blue",
            "back_image_url": "url_to_back_ice_blue",
        },
        {
            "name": "Heather Light Pink",
            "front_image_url": "url_to_front_heather_light_pink",
            "back_image_url": "url_to_back_heather_light_pink",
        },
        {
            "name": "Heather Forest Green",
            "front_image_url": "url_to_front_heather_forest_green",
            "back_image_url": "url_to_back_heather_forest_green",
        },
        {
            "name": "Charcoal",
            "front_image_url": "url_to_front_charcoal",
            "back_image_url": "url_to_back_charcoal",
        },
        {
            "name": "Sport Grey",
            "front_image_url": "url_to_front_sport_grey",
            "back_image_url": "url_to_back_sport_grey",
        },
        {
            "name": "Light Blue",
            "front_image_url": "url_to_front_light_blue",
            "back_image_url": "url_to_back_light_blue",
        },
        {
            "name": "Light Pink",
            "front_image_url": "url_to_front_light_pink",
            "back_image_url": "url_to_back_light_pink",
        },
        {
            "name": "Sand",
            "front_image_url": "url_to_front_sand",
            "back_image_url": "url_to_back_sand",
        },
        {
            "name": "Stone Blue",
            "front_image_url": "url_to_front_stone_blue",
            "back_image_url": "url_to_back_stone_blue",
        },
        {
            "name": "Military Green",
            "front_image_url": "url_to_front_military_green",
            "back_image_url": "url_to_back_military_green",
        },
        {
            "name": "White",
            "front_image_url": "url_to_front_white",
            "back_image_url": "url_to_back_white",
        },
        {
            "name": "Black",
            "front_image_url": "url_to_front_black",
            "back_image_url": "url_to_back_black",
        },
        {
            "name": "Navy",
            "front_image_url": "url_to_front_navy",
            "back_image_url": "url_to_back_navy",
        },
        {
            "name": "Carolina Blue",
            "front_image_url": "url_to_front_carolina_blue",
            "back_image_url": "url_to_back_carolina_blue",
        },
        {
            "name": "Irish Green",
            "front_image_url": "url_to_front_irish_green",
            "back_image_url": "url_to_back_irish_green",
        },
        {
            "name": "Purple",
            "front_image_url": "url_to_front_purple",
            "back_image_url": "url_to_back_purple",
        },
        {
            "name": "Red",
            "front_image_url": "url_to_front_red",
            "back_image_url": "url_to_back_red",
        },
        {
            "name": "Daisy",
            "front_image_url": "url_to_front_daisy",
            "back_image_url": "url_to_back_daisy",
        },
    ]

    for color_data in colors:
        color = Color(**color_data)
        db.session.add(color)
    db.session.commit()

def undo_seed_colors():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.colors RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM colors"))
        
    db.session.commit()
