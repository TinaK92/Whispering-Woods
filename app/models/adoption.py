from .db import db, environment, SCHEMA, add_prefix_for_prod
from .animal_category import animal_categories


class Adoption(db.Model):
    __tablename__ = "adoptions"
    if environment == "production":
        __table_args__ = {"schema": SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey(add_prefix_for_prod("users.id")), nullable=False
    )
    animal_name = db.Column(db.String(255), nullable=False)
    animal_age = db.Column(db.String(255), nullable=False)
    animal_color = db.Column(db.String(255), nullable=False)
    animal_breed = db.Column(db.String(255), nullable=False)
    animal_bio = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    adoption_fee = db.Column(db.Float, nullable=False, default=0.0) 
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(
        db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now()
    )

    # Still need relationships 
    user = db.relationship("User", back_populates="adoptions")

    categories = db.relationship('Category', secondary= animal_categories, back_populates='adoptions')

    images = db.relationship("AdoptionImage", back_populates="adoption", cascade="all, delete-orphan")


    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "animal_type": self.animal_name,
            "animal_age": self.animal_age,
            "animal_color": self.animal_color,
            "animal_breed": self.animal_breed,
            "animal_bio": self.animal_bio,
            "image_url": self.image_url,
            "adoption_fee": self.adoption_fee,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
