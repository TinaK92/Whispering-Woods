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
    quantity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now()
    )

    # Relationships:
    user = db.relationship("User", back_populates="listings")
    sizes = db.relationship(
        "Size",
        secondary="listing_sizes",  # Use the join table name as a string
        back_populates="listings",
    )

    colors = db.relationship(
        "Color",
        secondary="listing_colors",
        back_populates="listings",
        cascade="all"
    )
    images = db.relationship("Image", back_populates="listing", cascade="all, delete-orphan")

    cart_items = db.relationship('CartItem', back_populates='listing' )

    

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "description": self.description,
            "base_price": str(self.base_price),  # Convert to string for JSON serialization
            "sizes": [size.to_dict() for size in self.sizes],  # Assuming `Size` has a `to_dict` method
            "colors": [color.to_dict() for color in self.colors],  # Assuming `Color` has a `to_dict` method
            "images": [image.to_dict() for image in self.images],
            'quantity': self.quantity,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
