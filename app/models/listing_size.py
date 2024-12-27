from .db import db, environment, SCHEMA, add_prefix_for_prod

listing_sizes = db.Table(
    "listing_sizes",
    db.Model.metadata,
    db.Column("listing_id", db.Integer, db.ForeignKey(add_prefix_for_prod("listings.id")), primary_key=True),
    db.Column("size_id", db.Integer, db.ForeignKey(add_prefix_for_prod("sizes.id")), primary_key=True),
    schema=SCHEMA if environment == "production" else None  # Add schema for production
)