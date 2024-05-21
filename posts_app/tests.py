from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase

from posts_app.models import Posts


class PostsApiTestsPrivate(APITestCase):
    """
    Tests for posts api

    Current user is authenticated
    """

    base_url = "/posts/"

    def setUp(self):
        """
        Sets up authenticated user
        """
        MyUser = get_user_model()
        self.user = MyUser.objects.create_user(
            "authenticated_usere@mail.ru", "password"
        )
        self.second_user = MyUser.objects.create_user(
            "second_user@mail.ru", "password1234"
        )
        self.client.force_authenticate(user=self.user)

    def test_get_posts(self):
        """
        Ensure we can read all posts by GET request
        """
        status_code = self.client.get(self.base_url).status_code
        self.assertEqual(status_code, status.HTTP_200_OK)

    def test_create_post(self):
        """
        Ensure the authenticated user can create a new post by POST request
        """
        path_to_test_image = "./posts_app/defaultImage.jpeg"
        file = File(open(path_to_test_image, "rb"))
        uploaded_file = SimpleUploadedFile(
            "new_image.jpg", file.read(), content_type="multipart/form-data"
        )

        post_data = {
            "title": "Test Title",
            "text": "Post Text",
            "cover_path": uploaded_file,
            "tags": "tag1 tag2",
        }
        response = self.client.post(
            self.base_url, post_data, format="multipart"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def create_post(self) -> int:
        """
        Helper function that creates post and returns post_id
        """
        path_to_test_image = "./posts_app/defaultImage.jpeg"
        file = File(open(path_to_test_image, "rb"))
        uploaded_file = SimpleUploadedFile(
            "new_image.jpg", file.read(), content_type="multipart/form-data"
        )

        post_data = {
            "title": "Post for editing",
            "text": "Post for edit text",
            "cover_path": uploaded_file,
            "tags": "tag1 tag2",
        }
        self.client.post(self.base_url, post_data, format="multipart")
        post_id = Posts.objects.all()[0].id
        return post_id

    def test_edit_post(self):
        """
        Ensure that user can edit only those news that belong to him.

        But other users can't edit anothers users news
        """
        post_id = self.create_post()
        edited_post_data = {"title": "Edited Title"}
        response = self.client.patch(
            f"{self.base_url} {post_id}/", edited_post_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_another_user_post(self):
        """
        Ensure that user can't edit anothers users posts
        """
        post_id = self.create_post()
        self.client.force_authenticate(user=self.second_user)
        edited_post_data = {"title": "Edited Title"}
        response = self.client.patch(
            f"{self.base_url}{post_id}/", edited_post_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_post(self):
        """
        Ensure that user can delete only those news that belong to him

        However other users can't delete anothers users news
        """
        self.client.force_authenticate(user=self.user)
        post_id = self.create_post()
        response = self.client.delete(
            f"{self.base_url}{post_id}/", format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_another_user_post(self):
        """
        Ensure that user can't delete anothers users posts
        """
        post_id = self.create_post()
        self.client.force_authenticate(user=self.second_user)
        response = self.client.delete(
            f"{self.base_url}{post_id}/", format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
