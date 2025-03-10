from .db import db, environment, SCHEMA, add_prefix_for_prod


class AdoptionImage(db.Model):
    __tablename__ = "adoption_images"
    if environment == "production":
        __table_args__ = {"schema": SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    adoption_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod("adoptions.id")), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)

    adoption = db.relationship("Adoption", back_populates="images")

    def to_dict(self):
        return {"id": self.id, "image_url": self.image_url}