from flask import Blueprint, request
from app.models import Listing, db
from flask_login import current_user, login_required
from app.forms.listing_form import ListingForm
from app.api.aws_helpers import upload_file_to_s3, get_unique_filename, allowed_file
from dotenv import load_dotenv

# Loading my enviorment variables from my .env
load_dotenv()

listing_routes = Blueprint('listings', __name__)

# GET ALL LISTINGS -------------------------------
@listing_routes.route('/', methods=["GET"])
def get_all_listings():
    listings = Listing.query.all()
    all_listings = [listing.to_dict() for listing in listings]
    return all_listings

# GET A LISTING ----------------------------------
@listing_routes.route('/<int:id>', methods=["GET"])
def get_listing():
    listing = Listing.query.get(id)
    if listing:
        return listing.to_dict(), 200
    else:
        return {'error': "Listing was not found"}, 404
    
# CREATE NEW LISTING -----------------------------
@listing_routes.route('/new', methods=["PUT"])
@login_required
def create_listing():
    form = ListingForm()
    form['csrf_token'].data = request.cookies['csrf_token']

    if form.validate_on_submit():
        try:
            image = request.files.get('image')
            if not image:
                return ({"errors": "Image file is required"}), 400
            if not allowed_file(image.filename):
                return ({"errors": "File type not permitted"}), 400
            image.filename = get_unique_filename(image.filename)
            upload_result = upload_file_to_s3(image)

            if 'url' not in upload_result:  
                return ({"errors": upload_result.get('errors', 'File upload failed')}), 400
            
            new_listing = Listing(
                user_id=current_user.id,
                name=form.data['name'],
                description=form.data['description'],
                base_price=form.data['base_price'],
                image_url=upload_result['url']
            )
            db.session.add(new_listing)
            db.session.commit()
            return (new_listing.to_dict()), 201
        
        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            return ({"errors": "An error occurred while creating the listing. Please try again."}), 500

    else:
        return ({'errors': form.errors}), 400

# UPDATE A LISTING ----------------------------------------
@listing_routes.route('/<int:id>/edit', methods=["PUT"])
@login_required
def update_listing(id):
    listing = Listing.query.get(id)

    if not listing:
        return {'error': 'Listing not found'}, 404

    if listing.user_id != current_user.id:
        return {'error': 'Unauthorized'}, 403

    form = ListingForm()
    form['csrf_token'].data = request.cookies['csrf_token']

    if form.validate_on_submit():
        if form.image_url.data:  
            image = form.image_url.data
            if allowed_file(image.filename):
                image.filename = get_unique_filename(image.filename)
                upload_result = upload_file_to_s3(image)
                if 'url' not in upload_result:
                    return {"errors": upload_result.get('errors', 'File upload failed')}, 400
                listing.image_url = upload_result['url']

        # Update listing details
        listing.name = form.name.data
        listing.description = form.description.data
        listing.base_price = form.base_price.data
        
        db.session.commit()
        return listing.to_dict(), 200

    return {'errors': form.errors}, 400

# DELETE A LISTING ------------------------------------------
@listing_routes.route('/<int:id>', methods=["DELETE"])
@login_required
def delete_listing(id):
    listing = Listing.query.get(id)
    
    if not listing:
        return {'error': 'Listing not found'}, 404
    
    if listing.user_id != current_user.id:
        return {'error': 'Unauthorized'}, 403 
    
    db.session.delete(listing)
    db.session.commit()
    return {'message': 'Listing deleted successfully'}, 200