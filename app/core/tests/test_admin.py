from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

"""
Resources:

- Test client,
    https://docs.djangoproject.com/en/2.2/topics/testing/tools/#overview-and-a-quick-example

- Admin site urls (Django 2.1),
    https://docs.djangoproject.com/en/2.1/ref/contrib/admin/
"""


class AdminSiteTests(TestCase):

    def setUp(self):
        """
        A function to set up a test client, superuser and normal user
        for testing the admin site.
        """

        # Test client
        self.client = Client()

        # Admin user
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@django.com',
            password='testing321'
        )
        # Login to admin site with created superuser
        self.client.force_login(self.admin_user)

        # Normal user
        self.new_user = get_user_model().objects.create_user(
            email='new_user@django.com',
            password='testing321'
        )

    def test_users_listed(self):
        """ Test users are listed on user page. """

        # Create the url for the user page
        # See resources above
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.new_user.name)
        self.assertContains(res, self.new_user.email)

    def test_user_change_page(self):
        """ Test that the user edit page works. """

        # /admin/core/user/<ID>/
        url = reverse('admin:core_user_change', args=[self.new_user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """ Test that the create user page works. """

        # /admin/core/user/add/
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
