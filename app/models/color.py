from .db import db, environment, SCHEMA, add_prefix_for_prod

class Color(db.Model):
    __tablename__ = "colors"
    if environment == "production":
        __table_args__ = {"schema": SCHEMA}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)  # e.g., Red, Blue, Green
    front_image_url = db.Column(db.String(500), nullable=False)  # Front image for the color
    back_image_url = db.Column(db.String(500), nullable=False)   # Back image for the color

    # Relationship to Listings through the join table
    listings = db.relationship(
        "Listing",
        secondary="listing_colors",  # Specify the join table
        back_populates="colors"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "front_image_url": self.front_image_url,
            "back_image_url": self.back_image_url,
        }

