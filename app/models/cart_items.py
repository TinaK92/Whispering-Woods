from .db import db, environment, SCHEMA, add_prefix_for_prod


class CartItem(db.Model):
    __tablename__ = "cart_items"

    if environment == "production":
        __table_args__ = {"schema": SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(
        db.Integer, db.ForeignKey(add_prefix_for_prod("carts.id")), nullable=False
    )
    listing_id = db.Column(
        db.Integer, db.ForeignKey(add_prefix_for_prod("listings.id")), nullable=False
    )
    quantity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())

    cart = db.relationship("Cart", back_populates="cart_items")
    listing = db.relationship("Listing")

    def to_dict(self):
        return {
            "id": self.id,
            "cart_id": self.cart_id,
            "listing_id": self.listing_id,
            "quantity": self.quantity,
            "created_at": self.created_at,
            "listing": {
                "id": self.id,
                "user_id": self.user_id,
                "name": self.name,
                "description": self.description,
                "base_price": str(
                    self.base_price
                ),  # Convert to string for JSON serialization
                "sizes": [
                    size.to_dict() for size in self.sizes
                ],  # Assuming `Size` has a `to_dict` method
                "colors": [
                    color.to_dict() for color in self.colors
                ],  # Assuming `Color` has a `to_dict` method
                "images": [image.to_dict() for image in self.images],
                "created_at": self.created_at.isoformat() if self.created_at else None,
                "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            }
        }
