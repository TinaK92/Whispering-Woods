from .db import db, environment, SCHEMA, add_prefix_for_prod

class Cart(db.Model):
    __tablename__ = 'carts'

    if environment == 'production':
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())

    # Relationships
    user = db.relationship('User', back_populates='cart')
    cart_items = db.relationship('CartItem', back_populates='cart', cascade='all, delete orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'created_at': self.created_at,
            'cart_items': [item.to_dict() for item in self.cart_items] if self.cart_items else []
        }