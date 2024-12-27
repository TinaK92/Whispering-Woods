from .db import db, environment, SCHEMA, add_prefix_for_prod


class Listing(db.Model):
    __tablename__ = "listings"
    if environment == "production":
        __table_args__ = {"schema": SCHEMA}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey(add_prefix_for_prod("users.id")), nullable=False
    )
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    base_price = db.Column(db.Numeric(10, 2), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(
        db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now()
    )

    # Relationships:
    user = db.relationship("User", back_populates="listings")
    sizes = db.relationship(
        "Size",
        secondary="listing_sizes",  # Specify the join table
        back_populates="listings"
    )
    colors = db.relationship(
        "Color",
        secondary="listing_colors",  # Specify the join table
        back_populates="listings"
    )


    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "description": self.description,
            "base_price": str(self.base_price),
            "image_url": self.image_url,
            "sizes": [size.to_dict() for size in self.sizes],
            "colors": [color.to_dict() for color in self.colors],
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
