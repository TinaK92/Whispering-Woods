from .db import db, environment, SCHEMA, add_prefix_for_prod

class Size(db.Model):
    __tablename__ = "sizes"
    if environment == "production":
        __table_args__ = {"schema": SCHEMA}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)  # e.g., Small, Medium, Large

    # Relationship to Listings through the join table
    listings = db.relationship(
        "Listing",
        secondary="listing_sizes",  # Specify the join table
        back_populates="sizes"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }

