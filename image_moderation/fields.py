"""
Model fields for image moderation
"""
import boto3

from django.apps import AppConfig
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

_moderation_levels = {
    0: [],
    1: [
        'Visually Disturbing',
    ],
    2: [
        'Explicit Nudity',
        'Visually Disturbing',
        'Violence',
    ],
    3: [
        'Explicit Nudity',
        'Violence',
        'Visually Disturbing',
        'Gambling',
        'Hate Symbols',
    ],
    4: [
        'Explicit Nudity',
        'Suggestive',
        'Violence',
        'Visually Disturbing',
        'Rude Gestures',
        'Drugs',
        'Tobacco',
        'Alcohol',
        'Gambling',
        'Hate Symbols',
    ],
}


class ImageModerationField(models.ImageField):
    """
    Django Image Field child that adds
    image moderation functionality

    Must have IMAGE_MODERATION attribute in django project settings
    that should be a dictionary with AWS credentials
    """
    def __init__(
            self,
            moderation_level=4,
            min_confidence=60,
            custom_labels=None,
            not_appropiate_text=_('This image is not appropiate'),
            **kwargs,
        ):
        self.moderation_level = moderation_level
        self.custom_labels = custom_labels
        self.min_confidence = min_confidence
        self.not_appropiate_text = not_appropiate_text
        super().__init__(**kwargs)

    def moderate_image(self, image):
        """
        Function that receives image instance field instance
        as parameter, moderates the image with AWS's rekognition
        and returns if is appropiate
        """
        is_appropiate = True
        moderation_settings = getattr(settings, 'IMAGE_MODERATION')
        access_key = moderation_settings['AWS_ACCESS_KEY']
        secret_key = moderation_settings['AWS_SECRET_KEY']

        client = boto3.client(
            'rekognition',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name='us-east-1'
        )

        response = client.detect_moderation_labels(
            Image={
                'Bytes': image.read()
            }
        )

        if self.custom_labels is not None:
            comparison_labels = self.custom_labels
        else:
            comparison_labels = _moderation_levels.get(
                self.moderation_level,
                _moderation_levels[4]
            )

        for label in response['ModerationLabels']:
            if (
                label['Name'] in comparison_labels and
                label['Confidence'] > self.min_confidence
            ):
                is_appropiate = False

        return is_appropiate

    def validate(self, value, model_instance, **kwargs):
        is_appropiate = self.moderate_image(value)
        if not is_appropiate:
            raise ValidationError(self.not_appropiate_text)
        super().validate(value, model_instance, **kwargs)
