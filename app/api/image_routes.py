from flask import Blueprint, request, jsonify
from app.models import db, Image, Listing
from app.api.aws_helpers import upload_file_to_s3, allowed_file, get_unique_filename

image_routes = Blueprint('images', __name__)

# Route to upload an image
@image_routes.route('', methods=['POST'])
def upload_image():
    if "image" not in request.files:
        return {"errors": "Image file is required"}, 400

    image = request.files["image"]

    if not allowed_file(image.filename):
        return {"errors": "File type not allowed"}, 400

    image.filename = get_unique_filename(image.filename)
    upload = upload_file_to_s3(image)

    if "url" not in upload:
        # If the upload fails
        return upload, 400

    url = upload["url"]

    # Create an image record in the database
    listing_id = request.form.get("listing_id")  # Ensure the client sends this
    color_id = request.form.get("color_id")  # Ensure the client sends this

    if not listing_id or not color_id:
        return {"errors": "Listing ID and Color ID are required"}, 400

    new_image = Image(
        listing_id=listing_id,
        color_id=color_id,
        front_image_url=url,  # This assumes you're uploading a front image
        back_image_url=request.form.get("back_image_url")  # Optional back image
    )

    db.session.add(new_image)
    db.session.commit()

    return new_image.to_dict(), 201

# Route to delete an image
@image_routes.route('/<int:image_id>', methods=['DELETE'])
def delete_image(image_id):
    image = Image.query.get(image_id)

    if not image:
        return {"errors": "Image not found"}, 404

    db.session.delete(image)
    db.session.commit()

    return {"message": "Image deleted successfully"}, 200
