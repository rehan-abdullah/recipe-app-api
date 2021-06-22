from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='test_user@django.com', password='testing321'):
    """ Create a sample user """
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """ Test creating a new user with an email was successful. """

        # Test setup
        email = 'new_user@django.com'
        password = 'testing321'

        # Call the create_user function that will be implemented in
        # Model manager for the custom user model
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        # Run test
        self.assertEqual(user.email, email)

        # Passwords must be checked using the check_password function
        # as they are not stored in raw format.
        # check_password is a helper function that comes with
        # the Django user model.
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """ Test the email for a new user is normalized """
        email = 'new_user@DJANGO.COM'
        user = get_user_model().objects.create_user(
            email=email,
            password='testing321'
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """ Test creating user with no email raises error. """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'testing321')

    def test_create_new_superuser(self):
        """ Test that a new superuser was created. """

        user = get_user_model().objects.create_superuser(
            'admin@djano.com',
            'testing321'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """ Test the tag string representation """
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """ Test the ingredient string representation """
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Cucumber'
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """ Test the recipe string representation """
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='Moroccan Lamb Stew',
            time_minutes=5,
            price=5.00
        )

        self.assertEqual(str(recipe), recipe.title)

    # Overrides the uuid function that comes with the python library
    # so that the function can be 'mocked' for the test.
    @patch('uuid.uuid4')
    def test_recipe_filename_uuid(self, mock_uuid):
        """ Test that image is saved in the correct location. """

        uuid = 'test-uuid'
        # Mocks the uuid function
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'myimage.jpg')

        exp_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)
