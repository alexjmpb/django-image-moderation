============================
Django Image Moderation v0.1
============================

Django image moderation is a Django package that adds a automatic image moderation field.

This image moderation field works using AWS Rekognition service so you would have to configure your AWS credentials

To get started
--------------

To get started with Django image moderation run on your terminal the following command:

    ``$ pip install django-image-moderation``

After you installed the application, you also have to install the package boto3:

    ``$ pip install boto3``

And don't forget to check if you have Pillow installed, since is required by Django's ImageField.

Once you've installed all the requirements, you have to add the application to the installed apps of your project settings:

my_django_project/settings.py

.. code-block:: python

    INSTALLED_APPS= [
        ...
        'image_moderation',
    ]

You also have to create a new variable in settings.py called "IMAGE_MODERATION"
which should be a python dictionary containing the keys "AWS_ACCESS_KEY" and "AWS_SECRET_KEY"
with the respective AWS credentials:

my_django_project/settings.py

.. code-block:: python

    IMAGE_MODERATION= {
        'AWS_ACCESS_KEY': your_aws_access_key,
        'AWS_SECRET_KEY': your_aws_secret_key,
    }

Finally to use the model field to moderate images uploaded by users
you have to create a model like the following:

my_django_project/my_app/models.py

.. code-block:: python

    from django.db import models
    from image_moderation import ImageModerationField


    class ImageObject(models.Model):
        image = ImageModerationField(
            upload_to='images',
            moderation_level=2
        )

You can customize the parameters of the moderation with:

* moderation_level: provides fixed moderation levels from 0 to 4, where 0 is the most permissive, that detect different moderations labels. Number with 4 as default
* min_confidence: When AWS Rekognition analyses an image it returns the labels found in the image and how confident is the AI about each label, you can configure a mininum confidence value to determine if the label is valid. Number from 0 to 100 with 60 as default
* custom_labels: List with personalized Rekognition labels that you want to include. You can find the list of labels in `AWS Rekognition docs <https://docs.aws.amazon.com/rekognition/latest/dg/moderation.html>`_

Any feedback or suggestion is more than welcome.

Thanks, Alexander (`@alexjmpb <https://github.com/alexjmpb>`_)