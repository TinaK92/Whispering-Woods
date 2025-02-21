from .db import db, environment, SCHEMA, add_prefix_for_prod


class Image(db.Model):
    __tablename__ = "images"
    if environment == "production":
        __table_args__ = {"schema": SCHEMA}

    id = db.Column(db.Integer, primary_key=True, 
    autoincrement=True)
    listing_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod("listings.id")))
    color_id = db.Column(db.ForeignKey(add_prefix_for_prod("colors.id")), nullable=False)
    image_url = db.Column(db.String, nullable=False)
    front = db.Column(db.Boolean, nullable=False)
    back = db.Column(db.Boolean, nullable=False)

    # Relationships
    # listing = db.relationship("Listing", back_populates="images")
    colors = db.relationship("Color", back_populates="images")
    listing = db.relationship("Listing", back_populates="images")

    def to_dict(self):
        return {
            "id": self.id,
            "color_id": self.color_id,
            "image_url": self.image_url,
            "front": self.front,
            "back": self.back
        }