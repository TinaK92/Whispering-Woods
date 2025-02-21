from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField, SelectMultipleField, FieldList, FormField
from wtforms.validators import DataRequired, Optional, URL
from wtforms.widgets import FileInput
from .ImageUploadForm import ImageUploadForm

class ListingForm(FlaskForm):
    name = StringField("Listing Title", validators=[DataRequired()])
    description = TextAreaField("Listing Description", validators=[DataRequired()])
    base_price = DecimalField("Price", places=2, validators=[DataRequired()])
    sizes = SelectMultipleField("Sizes", coerce=int)  # Expecting a list of integers
    colors = SelectMultipleField("Colors", coerce=int)  # Expecting a list of integers
    images = FieldList(FormField(ImageUploadForm), min_entries=1)

    def __init__(self, *args, **kwargs):
        super(ListingForm, self).__init__(*args, **kwargs)
        from app.models import Size, Color

        # Dynamically populate size and color choices from the database
        self.sizes.choices = [(size.id, size.name) for size in Size.query.order_by(Size.name).all()]
        self.colors.choices = [(color.id, color.name) for color in Color.query.order_by(Color.name).all()]
