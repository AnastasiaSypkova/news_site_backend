from django.contrib.auth import get_user_model
from django.contrib.staticfiles import finders
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase


class CommentsApiTest(APITestCase):
    """
    Tests for comments api

    Comments are available only for authenticated users
    """

    base_url = "/comments/"

    def setUp(self):
        """
        Sets up authenticated user
        """
        MyUser = get_user_model()
        self.user = MyUser.objects.create_user(
            "authenticated_usere@mail.ru", "password"
        )
        self.client.force_authenticate(user=self.user)

    def create_post(self):
        """
        Helper function that creates post for commenting

        Returns post id
        """
        path_to_test_image = finders.find("defaultImage.jpeg")
        file = File(open(path_to_test_image, "rb"))
        uploaded_file = SimpleUploadedFile(
            "new_image.jpg", file.read(), content_type="multipart/form-data"
        )

        post_data = {
            "title": "Post Title",
            "text": "Post Text",
            "cover_path": uploaded_file,
            "tags": "tag1 tag2",
        }
        response = self.client.post("/posts/", post_data, format="multipart")
        post_id = response.data["id"]
        return post_id

    def test_create_comment_for_existing_post(self):
        """
        Test for comment creating for specific post with certain id
        """
        post_id = self.create_post()
        comment_data = {"text": "текст комментария", "post_id": post_id}
        response = self.client.post(self.base_url, comment_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
