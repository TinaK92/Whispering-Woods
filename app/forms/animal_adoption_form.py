from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Optional
from app.api.aws_helpers import ALLOWED_EXTENSIONS


class AnimalAdoptionForm(FlaskForm):
    animal_name = StringField('Animal Name', validators=[DataRequired()])
    animal_age = IntegerField('Animal Age', validators=[DataRequired()])
    animal_color = StringField('Color', validators=[DataRequired()])
    animal_breed = StringField('Breed', validators=[DataRequired()])
    animal_bio = TextAreaField('Animal Bio', validators=[DataRequired()])
    image_url = FileField("Image File", validators=[Optional(), FileAllowed(list(ALLOWED_EXTENSIONS))])
    category_id = IntegerField('Category', validators=[DataRequired()])
    

    def __init__(self, *args, **kwargs):
        super(AnimalAdoptionForm, self).__init__(*args, **kwargs)
        
