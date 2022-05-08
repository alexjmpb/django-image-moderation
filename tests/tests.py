"""
Test cases to test Image moderation field
"""
from django.test import TestCase
from django.core.files.storage import default_storage
from django.core.exceptions import ValidationError

from tests.models import (
    CustomLabelsImageObject,
    ImageObject
)


class ModerationTests(TestCase):
    """
    Test cases for image moderation field
    must have the correct named files for them to work
    """
    def setUp(self):
        self.nsfw_explicit_nudity = default_storage.open('tests/nsfw_explicit_nudity.jpg')
        self.nsfw_suggestive = default_storage.open('tests/nsfw_suggestive.jpg')
        self.nsfw_hate_symbols = default_storage.open('tests/nsfw_hate_symbols.jpg')
        self.sfw = default_storage.open('tests/sfw.jpg')

    def test_sfw_upload(self):
        obj = ImageObject(image=self.sfw)

        obj.full_clean()
        obj.save()

        self.assertTrue(obj.image, self.sfw)

        obj.image.delete()

    def test_nsfw_upload(self):
        obj = ImageObject(image=self.nsfw_suggestive)

        with self.assertRaises(ValidationError):
            obj.full_clean()

    def test_custom_labels_not_valid_upload(self):
        obj = CustomLabelsImageObject(image=self.nsfw_explicit_nudity)
        obj2 = CustomLabelsImageObject(image=self.nsfw_hate_symbols)

        with self.assertRaises(ValidationError):
            obj.full_clean()

        with self.assertRaises(ValidationError):
            obj2.full_clean()

    def test_custom_labels_valid_upload(self):
        obj = CustomLabelsImageObject(image=self.nsfw_suggestive)

        obj.full_clean()
        obj.save()

        self.assertTrue(obj.image, self.sfw)

        obj.image.delete()
