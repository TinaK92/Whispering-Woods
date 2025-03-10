from .db import db, environment, SCHEMA, add_prefix_for_prod

animal_categories = db.Table(
    'animal_categories',
    db.Model.metadata,
    db.Column('adoption_id', db.Integer, db.ForeignKey(add_prefix_for_prod('adoptions.id')), primary_key=True),
    db.Column('category_id', db.ForeignKey(add_prefix_for_prod('categories.id')), primary_key=True)
)

if environment == "production":
    animal_categories.schema = SCHEMA
