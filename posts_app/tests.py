from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase


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
