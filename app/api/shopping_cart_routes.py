from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import db, Cart, CartItem, Listing
from dotenv import load_dotenv

cart_routes = Blueprint('carts', __name__)

# Loading my environment variables from my .env
load_dotenv()

# GET CART 
@cart_routes.route('/<int:id>', methods=['GET'])
@login_required
def get_cart(id):
    cart = Cart.query.filter_by(user_id=id).first()

    if not cart: 
        cart = Cart(user_id=current_user.id)
    db.session.add(cart)
    db.session.commit()

    return jsonify(cart.to_dict()), 200

# ADD TO CART
@cart_routes.route('/add', methods=['POST'])
@login_required
def add_to_cart():
    try:
        data = request.get_json()
        print("📥 Incoming data:", data)

        listing_id = data.get('listing_id')
        quantity = data.get('quantity', 1)

        # Validate listing_id
        if not isinstance(listing_id, int):
            try:
                listing_id = int(listing_id)
            except (ValueError, TypeError):
                return jsonify({'error': 'Invalid listing ID'}), 400

        # Validate quantity
        if not isinstance(quantity, int) or quantity < 1:
            return jsonify({'error': 'Invalid quantity'}), 400

        # Get or create user's cart
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        if not cart:
            cart = Cart(user_id=current_user.id)
            db.session.add(cart)
            db.session.commit()

        # Get the listing
        listing = Listing.query.get(listing_id)
        if not listing:
            return jsonify({'error': 'Listing not found'}), 404

        if listing.quantity < quantity:
            return jsonify({'error': 'Quantity exceeds inventory'}), 400

        # Get or create cart item
        cart_item = CartItem.query.filter_by(cart_id=cart.id, listing_id=listing_id).first()
        if cart_item:
            if cart_item.quantity + quantity > listing.quantity:
                return jsonify({'error': 'Quantity too high'}), 400
            cart_item.quantity += quantity
        else:
            cart_item = CartItem(cart_id=cart.id, listing_id=listing.id, quantity=quantity)
            db.session.add(cart_item)

        # Update listing stock
        listing.quantity -= quantity

        db.session.commit()
        return jsonify(cart.to_dict()), 200

    except Exception as e:
        print("🔥 Error in add_to_cart:", str(e))
        return jsonify({'error': str(e)}), 500

# UPDATE CART ITEMS 
@cart_routes.route('/<int:item_id>', methods=['PUT'])
@login_required
def update_cart_item(item_id):
    data = request.json
    new_quantity = data.get("quantity")

    cart_item = CartItem.query.get(item_id)

    if not cart_item:
        return {'error': 'Cart item cannot be found'}, 404
    
    if cart_item.cart.user_id != current_user.id:
        return {'error': 'You are not authorized to make changes to this cart!'}, 403
    
    if new_quantity <= 0:
        return {'error': 'Quantity must be greater than 0'}, 400
    
    listing = Listing.query.get(cart_item.listing_id)

    if not listing:
        return {'error': 'The listing cannot be found'}, 404
    
    quantity_change = new_quantity - cart_item.quantity

    if listing.quantity < quantity_change:
        return {'error': 'Our current inventory is too low for this quantity.'}, 400
    
    listing.quantity -= quantity_change
    
    cart_item.quantity = new_quantity

    db.session.commit()
    return jsonify(cart_item.to_dict()), 200

# DELET AN ITEM FROM A CART
@cart_routes.route('/<int:item_id>', methods=['DELETE'])
@login_required
def delete_item(item_id):
    cart_item = CartItem.query.get(item_id)

    if not cart_item:
        return {'error': 'Item cannot be found in cart'}, 404
    
    if cart_item.cart.user_id != current_user.id:
        return {'error': 'You are not authorized to make changes to this cart'}, 403
    
    listing = Listing.query.get(cart_item.listing_id)

    if listing:
        listing.quantity += cart_item.quantity

    db.session.delete(cart_item)
    db.session.commit()

    return {'message': 'The item has been removed from the cart'}, 200

# CLEAR CART OF EVERYTHNG
@cart_routes.route('/clear', methods=['DELETE'])
@login_required
def clear_cart():
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if not cart:
        return { 'error': 'Cart was not found' }, 404
    
    for item in cart.cart_items:
        listing = Listing.query.get(item.listing_id)
        if listing:
            listing.quantity += item.quantity

    cart.cart_items.clear()
    db.session.commit()

    return {'message': 'Cart has been cleared'}, 200



