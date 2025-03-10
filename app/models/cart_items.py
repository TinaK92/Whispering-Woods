from .db import db, environment, SCHEMA, add_prefix_for_prod

class CartItem(db.Model):
    __tablename__ = 'cart_items'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('carts.id')), nullable=False)
    listing_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('listings.id')), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())

    cart = db.relationship('Cart', back_populates='cart_items')
    listing = db.relationship('Listing')

    def to_dict(self):
        return {
            'id': self.id,
            'cart_id': self.cart_id,
            'listing_id': self.listing_id,
            'quantity': self.quantity,
            'created_at': self.created_at,
            'listing': {
                'id': self.listing.id,
                'title': self.listing.title,
                'description': self.listing.description,
                'price': self.listing.price,
                'image_url': self.listing.image_url,
                'created_at': self.listing.created_at,
                'updated_at': self.listing.updated_at,
                # Add other listing fields as needed
            }
        }