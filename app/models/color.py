from .db import db, environment, SCHEMA, add_prefix_for_prod

class Color(db.Model):
    __tablename__ = "colors"
    if environment == "production":
        __table_args__ = {"schema": SCHEMA}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)


    # Relationship to Listings through the join table
    images = db.relationship(
        "Image",
        secondary="image_colors",
        back_populates="colors"
    )
    listings = db.relationship(
        "Listing",
        secondary="listing_colors",
        back_populates="colors",
    )


    def to_dict(self, include_images=False):
        color_dict=  {
            "id": self.id,
            "name": self.name,
        }
        if include_images:
            color_dict["images"] = [image.to_dict() for image in self.images]
        return color_dict

