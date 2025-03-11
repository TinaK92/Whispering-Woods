from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField,  IntegerField, SelectMultipleField, FormField, SelectField, FileField
from wtforms.validators import DataRequired, Optional, URL, NumberRange
from flask_wtf.file import FileRequired,FileAllowed

class ListingForm(FlaskForm):
    name = StringField("Listing Title", validators=[DataRequired()])
    description = TextAreaField("Listing Description", validators=[DataRequired()])
    base_price = DecimalField("Price", places=2, validators=[DataRequired()])
    quantity = IntegerField("Quantity", validators=[DataRequired(), NumberRange(min=1)])
    sizes = SelectMultipleField("Sizes", coerce=int)  # Expecting a list of integers
    color = SelectField("Color", coerce=int)  # Expecting a list of integers
    front_image = FileField("Front Image", validators=[FileRequired()])
    back_image = FileField("Back Image", validators=[FileRequired()])

    def __init__(self, *args, **kwargs):
        super(ListingForm, self).__init__(*args, **kwargs)
        from app.models import Size, Color

        # e.g., load all sizes
        self.sizes.choices = [
            (size.id, size.name)
            for size in Size.query.order_by(Size.name).all()
        ]

        # load all colors
        self.color.choices = [(c.id, c.name) for c in Color.query.all()]



        