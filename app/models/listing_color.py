from .db import db, environment, SCHEMA, add_prefix_for_prod

listing_colors = db.Table(
    "listing_colors",
    db.Model.metadata,
    db.Column(
        "listing_id",
        db.Integer,
        db.ForeignKey(add_prefix_for_prod("listings.id")),
        primary_key=True,
    ),
    db.Column(
        "color_id",
        db.Integer,
        db.ForeignKey(add_prefix_for_prod("colors.id")),
        primary_key=True,
    ),
    schema=SCHEMA if environment == "production" else None,  # Add schema for production
)
