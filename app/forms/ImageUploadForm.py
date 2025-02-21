from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.widgets import FileInput
from app.api.aws_helpers import ALLOWED_EXTENSIONS


# Subform for Image Uploads
class ImageUploadForm(FlaskForm):
    class Meta:
        csrf = False
        
    front_image = FileField(
        "Front Image",
        validators=[
            FileRequired(message="Front image is required."),
            FileAllowed(list(ALLOWED_EXTENSIONS), message="File type not allowed."),
        ],
    )
    back_image = FileField(
        "Back Image",
        widget=FileInput(),
        validators=[
            FileRequired(message="Back image is required."),
            FileAllowed(list(ALLOWED_EXTENSIONS), message="File type not allowed."),
        ],
    )
