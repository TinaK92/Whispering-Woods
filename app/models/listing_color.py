from sqlalchemy.schema import Table, Column
from sqlalchemy.sql.sqltypes import Integer
from .db import db, environment, SCHEMA, add_prefix_for_prod

listing_colors = Table(
    "listing_colors",
    db.Model.metadata,
    db.Column(
        "listing_id",
        Integer,
        db.ForeignKey(add_prefix_for_prod("listings.id")),
        primary_key=True,
    ),
    db.Column(
        "color_id",
        Integer,
        db.ForeignKey(add_prefix_for_prod("colors.id")),
        primary_key=True,
    ),
    schema=SCHEMA if environment == "production" else None,
)