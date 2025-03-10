from flask import Blueprint, request
from app.models import db, Adoption, Category, animal_categories
from flask_login import current_user, login_required
from app.api.aws_helpers import upload_file_to_s3, get_unique_filename, allowed_file
from app.forms.animal_adoption_form import AnimalAdoptionForm
from dotenv import load_dotenv


# Loading my environment variables from my .env
load_dotenv()

adoption_routes = Blueprint('adoptions', __name__)

# GET ALL ANIMALS UP FOR ADOPTIONS
@adoption_routes.route('/')
def get_all_adoptions():
    adoptions = Adoption.query.all()
    adoption_list = [adoption.to_dict() for adoption in adoptions]
    return adoption_list

# GET ALL ANIMALS THAT ARE UP FOR ADOPTION
@adoption_routes.route('/adoption/<int:user_id>')
def get_user_adoptions(user_id):
    adoptions = Adoption.query.filter_by(user_id=user_id).all()
    return {'adoptions': [adoption.to_dict() for adoption in adoptions]}

# GET A SPECIFIC ANIMAL ADOPTION
@adoption_routes.route('/<int:id>')
def get_adoption(id):
    animal = Adoption.query.get(id)
    if animal:
        return animal.to_dict(), 200
    else:
        return {'error': 'Adoption not found'}, 404
    
# CREATE NEW ANIMAL ADOPTION
@adoption_routes.route('/new', methods=['POST'])
@login_required
def create_animal_adoption():
    form = AnimalAdoptionForm()
    form['csrf_token'].data = request.cookies['csrf_token']

    if form.validate_on_submit():
        try:
            image = request.files.get('image')
            if not image:
                return ({"errors": "Image file is required"}), 400
            
            if not allowed_file(image.filename):
                return ({"errors": "File type not permitted"}), 400
            
            image.filename = get_unique_filename(image.filename)
            upload_image = upload_file_to_s3(image)

            if 'url' not in upload_image:
                return ({"errors": upload_image.get('errors', 'File upload failed')}), 400
            
            new_animal = Adoption(
                user_id=current_user.id,
                animal_name=form.data['animal_name'],
                animal_age=form.data['animal_age'],
                animal_color=form.data['animal_color'],
                animal_breed=form.data['animal_breed'],
                animal_bio=form.data['animal_bio'],
                image_url=upload_image['url']
            )

            db.session.add(new_animal)
            db.session.commit()

            return (new_animal.to_dict()), 201
        
        except Exception as e:
            db.session.rollback() 
            return ({"errors": "An error occurred while creating the new animal adoption. Please Try again."}), 500
        
    else:
        return ({"errors": form.errors}), 400
    
# UPDATE ANIMAL ADOPTION
@adoption_routes.route('/<int:id>/edit', methods=['PUT'])
@login_required
def update_adoption(id):
    adoption = Adoption.query.get(id)

    if not adoption:
        return {'error': 'Animal not found'}, 404
    
    if adoption.user_id != current_user.id:
        return {'error': 'Unauthorized'}, 403 
    
    form = AnimalAdoptionForm()
    form['csrf_token'].data = request.cookies['csrf_token']

    if form.validate_on_submit():
        if form.image_url.data:
            image = form.image_url.data
            if allowed_file(image.filename):
                image.filename = get_unique_filename(image.filename)
                upload_image = upload_file_to_s3(image)
                if 'url' not in upload_image:
                    return {"errors": upload_image.get('errors', 'File upload failed')}, 400
                adoption.image_url = upload_image['url']

        
        adoption.animal_name = form.animal_name.data
        adoption.animal_age = form.animal_age.data
        adoption.animal_color = form.animal_color.data
        adoption.animal_breed = form.animal_breed.data
        adoption.animal_bio = form.animal_bio.data
        adoption.image_url = form.image_url.data

        db.session.commit()
        return adoption.to_dict(), 200

    return {'errors': form.errors}, 400


# DELETE AN ANIMAL 
@adoption_routes.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_adoption(id):
    adoption = Adoption.query.get(id)

    if not adoption:
        return {'error': 'Animal not found'}, 404
    
    if adoption.user_id != current_user.id:
        return {'error': 'Unauthorized'}, 403
    
    db.session.execute()
    # do i have to delete the category 
    db.session.delete(adoption)
    db.session.commit()
    return {'message': 'Adoption deleted succesfully'}, 200

