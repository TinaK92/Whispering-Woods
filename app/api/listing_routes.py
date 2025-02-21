from flask import Blueprint, request, jsonify, current_app as app
from app.models import Listing, db, Color, Size, Image
from flask_login import current_user, login_required
from app.forms.listing_form import ListingForm
from app.forms.ImageUploadForm import ImageUploadForm
from dotenv import load_dotenv

# Loading my environment variables from my .env
load_dotenv()

listing_routes = Blueprint("listings", __name__)


# GET ALL LISTINGS -------------------------------
@listing_routes.route("/", methods=["GET"])
def get_all_listings():
    listings = Listing.query.all()
    all_listings = [listing.to_dict() for listing in listings]
    return all_listings


# GET A LISTING ----------------------------------
@listing_routes.route("/<int:id>", methods=["GET"])
def get_listing(id):
    listing = Listing.query.get(id)
    if listing:
        return listing.to_dict(), 200
    else:
        return {"error": "Listing was not found"}, 404


# CREATE NEW LISTING -----------------------------
@listing_routes.route("/new", methods=["POST"])
@login_required
def create_listing():
    print("Request form data:", request.form)
    print("Request files:", request.files)

    form = ListingForm()
    form['csrf_token'].data = request.cookies['csrf_token']

    if not form.validate_on_submit():
        print("Form validation errors:", form.errors)
        return {"errors": form.errors}, 400

    try:
        # 🔹 Check that images are present before validation
        if "front_image" not in request.files or "back_image" not in request.files:
            return {"errors": {"images": ["Front and back images are required."]}}, 400

        front_image_file = request.files["front_image"]
        back_image_file = request.files["back_image"]

        # 🔹 Validate Image Form
        image_form = ImageUploadForm()
        image_form['csrf_token'].data = request.cookies['csrf_token']
        image_form.front_image.data = front_image_file
        image_form.back_image.data = back_image_file

        if not image_form.validate():
            print("Image Form Errors:", image_form.errors)
            return {"errors": image_form.errors}, 400

        # 🔹 Upload to S3
        uploaded_front = upload_file_to_s3(front_image_file)
        uploaded_back = upload_file_to_s3(back_image_file)

        if "url" not in uploaded_front or "url" not in uploaded_back:
            return {"errors": "File upload failed."}, 400

        # 🔹 Create Listing
        listing = Listing(
            user_id=current_user.id,
            name=form.name.data,
            description=form.description.data,
            base_price=form.base_price.data
        )
        db.session.add(listing)
        db.session.flush()

        # 🔹 Save Images with Correct Associations
        front_image = Image(
            listing_id=listing.id,
            color_id=form.colors.data[0],  # Ensure this is correctly assigned
            image_url=uploaded_front["url"],
            front=True,
            back=False
        )
        back_image = Image(
            listing_id=listing.id,
            color_id=form.colors.data[0],
            image_url=uploaded_back["url"],
            front=False,
            back=True
        )
        db.session.add(front_image)
        db.session.add(back_image)

        db.session.commit()
        return {"message": "Listing created successfully", "listing": listing.to_dict()}, 201

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error creating listing: {e}")
        return {"errors": "An error occurred while creating the listing."}, 500


# UPDATE A LISTING ----------------------------------------
@listing_routes.route("/<int:id>/edit", methods=["PUT"])
@login_required
def update_listing(id):
    listing = Listing.query.get(id)

    if not listing:
        return {"error": "Listing not found"}, 404

    if listing.user_id != current_user.id:
        return {"error": "Unauthorized"}, 403

    form = ListingForm()
    form["csrf_token"].data = request.cookies["csrf_token"]

    if form.validate_on_submit():
        # Update listing details
        listing.name = form.name.data
        listing.description = form.description.data
        listing.base_price = form.base_price.data

        # Update sizes
        listing.sizes = []
        for size_id in form.sizes.data:
            size = Size.query.get(size_id)
            if size:
                listing.sizes.append(size)

        # Update colors
        listing.colors = []
        for color_id in form.colors.data:
            color = Color.query.get(color_id)
            if color:
                listing.colors.append(color)

        db.session.commit()
        return listing.to_dict(), 200

    return {"errors": form.errors}, 400


# DELETE A LISTING ------------------------------------------
@listing_routes.route("/<int:id>", methods=["DELETE"])
@login_required
def delete_listing(id):
    listing = Listing.query.get(id)

    if not listing:
        return {"errors": "Listing not found"}, 404

    if listing.user_id != current_user.id:
        return {"errors": "Unauthorized"}, 403

    # Delete listing
    db.session.delete(listing)
    db.session.commit()

    return {"message": "Listing deleted successfully"}, 200
