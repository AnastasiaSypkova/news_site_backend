from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase


class UsersManagersTests(TestCase):
    """
    Tests for custom user manager
    """

    def test_create_user(self):
        """
        Test for creating a simple user
        """
        MyUser = get_user_model()
        user = MyUser.objects.create_user(
            email="normal@user.com", password="foo"
        )
        self.assertEqual(user.email, "normal@user.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            MyUser.objects.create_user()
        with self.assertRaises(ValueError):
            MyUser.objects.create_user(email="")
        with self.assertRaises(ValueError):
            MyUser.objects.create_user(email="", password="foo")

    def test_create_superuser(self):
        """
        Test for creating a superuser
        """
        User = get_user_model()
        admin_user = User.objects.create_superuser("super@mail.ru", "foo")
        self.assertEqual(admin_user.email, "super@mail.ru")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="super@mail.ru", password="foo", is_superuser=False
            )


class UserApiTests(APITestCase):
    """
    Tests for user api
    """

    base_url = "/users/"

    def test_get_users(self):
        """
        Ensure we can read all users by GET request
        """
        status_code = self.client.get(self.base_url).status_code
        self.assertEqual(status_code, status.HTTP_200_OK)

    def test_create_user(self):
        """
        Ensure we can create a new user by POST request
        """
        User = get_user_model()
        user = User.objects.create_user(
            email="normal@user.com", password="foo"
        )
        self.client.force_authenticate(user)
        users_list = self.client.get(self.base_url).data
        initial_len = len(users_list)

        data = {"email": "new_user@maail.com", "password": "password"}
        response = self.client.post(self.base_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        users_list = self.client.get(self.base_url).data
        self.assertEqual(len(users_list), initial_len + 1)

        self.assertEqual(User.objects.last().email, "new_user@maail.com")
