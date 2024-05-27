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

        self.assertIsNone(user.username)

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
        MyUser = get_user_model()
        admin_user = MyUser.objects.create_superuser("super@mail.ru", "foo")
        self.assertEqual(admin_user.email, "super@mail.ru")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

        self.assertIsNone(admin_user.username)
        with self.assertRaises(ValueError):
            MyUser.objects.create_superuser(
                email="super@mail.ru", password="foo", is_superuser=False
            )


class UserApiTestsPrivate(APITestCase):
    """
    Tests for user api

    The user is authenticated
    """

    base_url = "/users/"

    def setUp(self):
        MyUser = get_user_model()
        self.user = MyUser.objects.create_user(
            "test_user_private@mail.ru", "foo"
        )
        self.another_user = MyUser.objects.create_user(
            "test_other_private@mail.ru", "fooother"
        )
        self.client.force_authenticate(user=self.user)

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
        MyUser = get_user_model()

        users_list = self.client.get(self.base_url).data
        initial_len = users_list["total"]

        data = {"email": "new_user@maail.com", "password": "password"}
        response = self.client.post(self.base_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        users_list = self.client.get(self.base_url).data
        self.assertEqual(users_list["total"], initial_len + 1)

        self.assertEqual(MyUser.objects.last().email, "new_user@maail.com")

    def test_update_user(self):
        """
        Ensure the user can update its own profile
        Other users can't update another's users profiles
        """

        data = {"first_name": "edited_name", "last_name": "edited_lastname"}
        response = self.client.patch(
            f"{self.base_url} {self.user.id}/", data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_another_user(self):
        """
        Ensure users can't update another's users profiles
        """
        data = {"first_name": "edited_name", "last_name": "edited_lastname"}
        response = self.client.patch(
            f"{self.base_url} {self.another_user.id}/", data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_user(self):
        """
        Ensure that user can delete its own profile
        Other users can't delete another's users profiles
        """
        response = self.client.delete(
            f"{self.base_url} {self.user.id}/", format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_another_user(self):
        """
        Ensure that user can't delete another's users profiles
        """
        response = self.client.delete(
            f"{self.base_url} {self.another_user.id}/", format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UserApiTestsPublic(APITestCase):
    """
    Tests for user api

    The user is unauthenticated
    """

    base_url = "/users/"

    def setUp(self):
        MyUser = get_user_model()
        self.user = MyUser.objects.create_superuser(
            "test_user_private@mail.ru", "foo"
        )

    def test_update_user(self):
        """
        Ensure the user can't send PATCH request if he is anauthenticated
        """

        data = {"first_name": "edited_name", "last_name": "edited_lastname"}
        response = self.client.patch(
            f"{self.base_url} {self.user.id}/", data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_user(self):
        """
        Ensure the user can't send DELETE request if he is anauthenticated
        """
        response = self.client.delete(
            f"{self.base_url} {self.user.id}/", format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_users(self):
        """
        Ensure we can read all users by GET request if we anonymous
        """
        status_code = self.client.get(self.base_url).status_code
        self.assertEqual(status_code, status.HTTP_200_OK)

    def test_create_user(self):
        """
        Ensure we can create a new user by POST request if we anonymous
        """
        MyUser = get_user_model()

        users_list = self.client.get(self.base_url).data
        initial_len = users_list["total"]

        data = {"email": "new_user@maail.com", "password": "password"}
        response = self.client.post(self.base_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        users_list = self.client.get(self.base_url).data
        self.assertEqual(users_list["total"], initial_len + 1)

        self.assertEqual(MyUser.objects.last().email, "new_user@maail.com")
