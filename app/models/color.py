from .db import db, environment, SCHEMA, add_prefix_for_prod

class Color(db.Model):
    __tablename__ = "colors"
    if environment == "production":
        __table_args__ = {"schema": SCHEMA}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    listings = db.relationship(
        "Listing",
        secondary="listing_colors",
        back_populates="colors"
    )

    images  = db.relationship("Image", back_populates="color", cascade="all, delete-orphan")


    def to_dict(self, include_images=False):
        color_dict=  {
            "id": self.id,
            "name": self.name,
        }
        return color_dict

