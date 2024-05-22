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
            "authenticated_usere@mail.ru",
            "password",
            first_name="Masha",
            last_name="Ivanova",
        )
        self.second_user = MyUser.objects.create_user(
            "second_user@mail.ru",
            "password1234",
            first_name="Ivan",
            last_name="Petrov",
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

    def create_post(self, title="Post title", text="Post text") -> int:
        """
        Helper function that creates post and returns post_id
        """
        path_to_test_image = "./posts_app/defaultImage.jpeg"
        file = File(open(path_to_test_image, "rb"))
        uploaded_file = SimpleUploadedFile(
            "new_image.jpg", file.read(), content_type="multipart/form-data"
        )

        post_data = {
            "title": title,
            "text": text,
            "cover_path": uploaded_file,
            "tags": "tag1 tag2",
        }
        self.client.post(self.base_url, post_data, format="multipart")
        post_id = Posts.objects.first().id
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

    def test_pagination(self):
        """
        Test pagination with limit and offset params

        example: GET /posts/?limit=2&offset=2
        """
        limit = 2
        offset = 2
        paginated_url = f"{self.base_url}?{limit=}&{offset=}"
        for i in range(limit * offset):
            _ = self.create_post()
        response = self.client.get(paginated_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], limit * offset)
        self.assertEqual(len(response.data["results"]), limit)

    def test_filter_posts_by_author(self):
        """
        Test filtering posts in GET request by author

        Author can be either last name or first name

        example: GET /posts/?author=Masha
        """
        self.client.force_authenticate(self.user)
        _ = self.create_post(title=f"{self.user.first_name}' Post")
        _ = self.create_post(title=f"{self.user.first_name}' Post")

        self.client.force_authenticate(self.second_user)
        _ = self.create_post(title=f"{self.second_user.first_name}' Post")

        response = self.client.get(
            f"{self.base_url}?author={self.user.first_name}"
        )
        self.assertEqual(len(response.data), 2)

        response = self.client.get(
            f"{self.base_url}?author={self.second_user.first_name}"
        )
        self.assertEqual(len(response.data), 1)

    def test_filter_posts_by_author_id(self):
        """
        Test filtering posts in GET request by author id

        example: GET /posts/?authorId=31
        """
        self.client.force_authenticate(self.user)
        _ = self.create_post(title=f"{self.user.first_name}' Post")
        _ = self.create_post(title=f"{self.user.first_name}' Post")

        self.client.force_authenticate(self.second_user)
        _ = self.create_post(title=f"{self.second_user.first_name}' Post")

        response = self.client.get(f"{self.base_url}?authorId={self.user.id}")
        self.assertEqual(len(response.data), 2)

        response = self.client.get(
            f"{self.base_url}?authorId={self.second_user.id}"
        )
        self.assertEqual(len(response.data), 1)

    def test_filter_posts_by_author_email(self):
        """
        Test filtering posts in GET request by author email

        example: GET /posts/?email=ivan.ivanov@mail.ru
        """
        self.client.force_authenticate(self.user)
        _ = self.create_post(title=f"{self.user.first_name}' Post")
        _ = self.create_post(title=f"{self.user.first_name}' Post")

        self.client.force_authenticate(self.second_user)
        _ = self.create_post(title=f"{self.second_user.first_name}' Post")

        response = self.client.get(f"{self.base_url}?email={self.user.email}")
        self.assertEqual(len(response.data), 2)

        response = self.client.get(
            f"{self.base_url}?email={self.second_user.email}"
        )
        self.assertEqual(len(response.data), 1)

    def test_search(self):
        """
        Test searching by search string in post title or post text via GET request

        example: GET /posts/?search=маргаритки
        """
        self.client.force_authenticate(self.user)
        _ = self.create_post(
            title="Новость про радугу",
            text="""
                              Радуга это красивое оптическое явление.
                              Увидеть радугу можно после дождя,
                              когда солнечные лучи преломляются на маленьких капельках,
                              играющих роль миниатюрных призмочек.
                              Солнечный свет раскладывается в спектр (прямо как Ньютон,
                              только вместо призмы -- водяные капли)
                             """,
        )

        _ = self.create_post(
            title="Планетарные туманности",
            text="""
                                Красивая штука, но вопреки названию ничего общего с планетами не имеют.
                                Это -- конец эволюции маломассивных звезд.
                                Когда в звезде выгорает водород и гелий,
                                а что-то тяжелее гелия загореться не может,
                                т.к. наша звезда -- миниатюрная (массы не достаточно)

                                Термоядерный синтез не идет. Ничего не горит.
                                И звезду раздувает до стадии красного гиганта
                                (гравитация слабенькая у нее,
                                сила газового давления сильнее гравитационного притяжения)

                                Звезда не способна удержать свою внешнюю обочку
                                Потом звезда теряет внешние слои и схлопывается до
                                белого карлика.
                                Вокруг нее остается газовая обочка -- планетарная туманность.
                                Поскольку там высокая степень ионизации это все очень красиво светится
                                в рентгене и в ик и в остальных диапазонах спектра
                                """,
        )

        response = self.client.get(
            f"{self.base_url}?search=Термоядерный синтез"
        )
        self.assertEqual(response.data[0]["title"], "Планетарные туманности")

        response = self.client.get(f"{self.base_url}?search=Ньютон")
        self.assertEqual(response.data[0]["title"], "Новость про радугу")


class PostsApiTestsPublic(APITestCase):
    """
    Tests for posts api where the user is unauthenticated
    """

    base_url = "/posts/"

    def test_get_posts(self):
        """
        Ensure we can read all posts by GET request if we anonymous
        """
        status_code = self.client.get(self.base_url).status_code
        self.assertEqual(status_code, status.HTTP_200_OK)

    def test_create_post(self):
        """
        Ensure the unauthenticated user can't create a new post by POST request
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
        response = self.client.post(
            self.base_url, post_data, format="multipart"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def create_post(self) -> int:
        """
        Helper function creates authenticated user that creates post

        Returns post id
        """
        MyUser = get_user_model()
        self.user = MyUser.objects.create_user(
            "authenticated_usere@mail.ru", "password"
        )
        self.client.force_authenticate(user=self.user)
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
        post_id = Posts.objects.first().id
        self.client.logout()
        return post_id

    def test_edit_post(self):
        """
        Ensure the user can't send PATCH request if he is unauthenticated
        """
        post_id = self.create_post()
        edited_post_data = {"title": "Edited Title"}
        response = self.client.patch(
            f"{self.base_url} {post_id}/", edited_post_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_post(self):
        """
        Ensure that user can't send DELETE request if he is unauthenticated
        """
        post_id = self.create_post()
        response = self.client.delete(
            f"{self.base_url}{post_id}/", format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
