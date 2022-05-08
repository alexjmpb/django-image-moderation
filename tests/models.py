from django.db import models

from image_moderation import (
    ImageModerationField,
)

def image_directory_path(instance, filename):
    return f'images/{filename}'


class ImageObject(models.Model):
    image = ImageModerationField(
        upload_to=image_directory_path,
        moderation_level=4,
        min_confidence=60
    )


class CustomLabelsImageObject(models.Model):
    image = ImageModerationField(
        upload_to=image_directory_path,
        moderation_level=5,
        min_confidence=60,
        custom_labels=[
            'Explicit Nudity',
            'Hate Symbols',
        ]
    )
