from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField,
    TextAreaField,
    DecimalField,
    IntegerField,
    SelectMultipleField,
)
from wtforms.validators import DataRequired, Optional
from app.api import ALLOWED_EXTENSIONS


class ListingForm(FlaskForm):
    name = StringField("Listing Title", validators=[DataRequired()])
    description = TextAreaField("Listing Description", validators=[DataRequired()])
    base_price = DecimalField("Price", places=2, validators=[DataRequired()])
    quantity = IntegerField("Quantity", validators=[DataRequired()])
    image_url = FileField(
        "Image File", validators=[Optional(), FileAllowed(list(ALLOWED_EXTENSIONS))]
    )
