from .db import db, environment, SCHEMA, add_prefix_for_prod
from .animal_category import animal_categories

class Category(db.Model):
    __tablename__ = 'categories'
    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

    adoptions = db.relationship('Adoption', secondary=animal_categories, back_populates='categories')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
        }