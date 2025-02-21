from sqlalchemy.schema import Table, Column
from sqlalchemy.sql.sqltypes import Integer
from .db import db, environment, SCHEMA, add_prefix_for_prod


image_colors = Table(
    "image_colors",
    db.Model.metadata,
    db.Column(
        "image_id",
        db.Integer,
        db.ForeignKey(add_prefix_for_prod("images.id")),
        primary_key=True,
    ),
    db.Column(
        "color_id",
        db.Integer,
        db.ForeignKey(add_prefix_for_prod("colors.id")),
        primary_key=True,
    ),
)

if environment == "production":
    image_colors.schema = SCHEMA