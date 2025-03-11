from flask import Blueprint, request, jsonify, current_app as app
from app.models import Listing, db, Color, Size, Image
from flask_login import current_user, login_required
from app.forms.listing_form import ListingForm
from dotenv import load_dotenv
from app.api.aws_helpers import upload_file_to_s3, get_unique_filename

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
    # print("Request form data:", request.form)
    # print("Request files:", request.files)

    form = ListingForm()
    form["csrf_token"].data = request.cookies["csrf_token"]

    if not form.validate_on_submit():
        print("Form validation errors:", form.errors)
        return {"errors": form.errors}, 400

    front_file = form.front_image.data
    if not front_file:
        return {"errors": {"images": "Front file is missing"}}, 400
    back_file = form.back_image.data
    if not back_file:
        return {"errors": {"images": "Back file is missing"}}, 400

    listing = Listing(
        user_id=current_user.id,
        name=form.name.data,
        description=form.description.data,
        base_price=form.base_price.data,
        quantity=form.quantity.data,
    )
    db.session.add(listing)
    db.session.flush()

    for size_id in form.sizes.data:
        size_obj = Size.query.get(size_id)
        if size_obj:
            listing.sizes.append(size_obj)

    color_id = form.color.data
    color_obj = Color.query.get(color_id)
    if not color_obj:
        return {"errors": {"color": "Invalid color chosen"}}, 400

    # if not front_file or back_file:
    #     return {"errors": {"images": "Front and back images are required"}}, 400

    front_filename = get_unique_filename(front_file.filename)
    back_filename = get_unique_filename(back_file.filename)
    front_file.filename = front_filename
    back_file.filename = back_filename
    uploaded_front = upload_file_to_s3(front_file)
    uploaded_back = upload_file_to_s3(back_file)

    front_image = Image(
        listing_id=listing.id,
        color_id=color_obj.id,
        image_url=uploaded_front["url"],
        front=True,
        back=False,
    )
    back_image = Image(
        listing_id=listing.id,
        color_id=color_obj.id,
        image_url=uploaded_back["url"],
        
        front=False,
        back=True,
    )
    db.session.add(front_image)
    db.session.add(back_image)

    db.session.commit()

    return {
        "message": "Listing created successfully",
        "listing": listing.to_dict(),
    }, 201


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
        # color_id = form.color.data
        # color_obj = Color.query.get(color_id)
        # if not color_obj:
        #     return {"errors": {"color": "Invalid color chosen"}}, 400
        
        # front_image = Image.query.get(listing.id)
        # front_image.color_id = color_id
        # back_image = Image.query.get(listing.id)
        # back_image.color_id = color_id

        # Update color
        color_id = form.color.data
        color_obj = Color.query.get(color_id)
        if not color_obj:
            return {"errors": {"color": "Invalid color chosen"}}, 400

        # Update front image color
        front_image = Image.query.filter_by(listing_id=listing.id, front=True).first()
        if front_image:
            front_image.color_id = color_id

        # Update back image color
        back_image = Image.query.filter_by(listing_id=listing.id, back=True).first()
        if back_image:
            back_image.color_id = color_id

        # db.session.add(front_image)
        # db.session.add(back_image)

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
