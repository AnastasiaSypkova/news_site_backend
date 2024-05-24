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
        self.second_user = MyUser.objects.create_user(
            "second_user@mail.ru", "password"
        )
        self.client.force_authenticate(user=self.user)

    def create_post(self) -> int:
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

    def create_comment(self, post_id: int) -> int:
        """
        Helper function that creates comment to the post

        Returns comment id
        """
        comment_data = {"text": "текст комментария", "post_id": post_id}
        create_comment_response = self.client.post(
            self.base_url, comment_data, format="json"
        )

        comment_id = create_comment_response.data["id"]
        return comment_id

    def test_create_comment_for_existing_post(self):
        """
        Test for comment creating for specific post with certain id
        """
        post_id = self.create_post()
        comment_data = {"text": "текст комментария", "post_id": post_id}
        response = self.client.post(self.base_url, comment_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_comment_for_non_existing_post(self):
        """
        Test creating comment for non valid id
        """
        post_id = 351

        comment_data = {"text": "текст комментария", "post_id": post_id}
        response = self.client.post(self.base_url, comment_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_comment(self):
        """
        Ensure we can read all comments by GET request
        """
        status_code = self.client.get(self.base_url).status_code
        self.assertEqual(status_code, status.HTTP_200_OK)

    def test_edit_comment(self):
        """
        Ensure the comment author can edit his comment
        """
        post_id = self.create_post()
        comment_id = self.create_comment(post_id)
        edited_comment_data = {
            "text": "отредактированный текст комментария",
            "post_id": post_id,
        }
        edit_comment_response = self.client.patch(
            f"{self.base_url} {comment_id}/",
            edited_comment_data,
            format="json",
        )
        self.assertEqual(edit_comment_response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            edit_comment_response.data["text"],
            "отредактированный текст комментария",
        )

    def test_edit_another_user_comment(self):
        """
        Ensure that user can't edit anothers users comments
        """
        post_id = self.create_post()
        comment_id = self.create_comment(post_id)

        self.client.force_authenticate(user=self.second_user)
        edited_comment_data = {
            "text": "пытаемся отредактировать чужой комментарий",
            "post_id": post_id,
        }
        edit_comment_response = self.client.patch(
            f"{self.base_url} {comment_id}/",
            edited_comment_data,
            format="json",
        )
        self.assertEqual(
            edit_comment_response.status_code, status.HTTP_403_FORBIDDEN
        )

    def test_delete_comment(self):
        """
        Ensure that comment author can delete its comment
        """
        post_id = self.create_post()
        comment_id = self.create_comment(post_id)

        response = self.client.delete(
            f"{self.base_url} {comment_id}/", format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_other_comment(self):
        """
        Ensure that user can't delete anothers users comments
        """
        post_id = self.create_post()
        comment_id = self.create_comment(post_id)

        self.client.force_authenticate(user=self.second_user)
        response = self.client.delete(
            f"{self.base_url} {comment_id}/", format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
