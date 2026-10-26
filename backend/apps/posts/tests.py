from django.test import TestCase
from apps.accounts.models import User
from apps.posts.models import Post
from django.test.utils import CaptureQueriesContext
from django.db import connection
from rest_framework.test import APITestCase
from rest_framework import status


# Create your tests here.


class PostAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@gmail.com",
            password="testuser123"
        )
        self.other_user = User.objects.create_user(
            username="anotheruser",
            email="anotheruser@example.com",
            password="anotherUser123"
        )

        self.posts_url = "/api/posts/"

        self.post = Post.objects.create(
            title="My original post",
            body="This belongs to testuser.",
            author=self.user
        )

        self.detail_url = f"/api/posts/{self.post.id}/"

    def test_anyone_can_view_posts(self):
        response = self.client.get(self.posts_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_user_cannot_create_post(self):
        # self.client.force_authenticate(self.user)

        response = self.client.post(
            self.posts_url,
            {
                "title": "My first post",
                "body": "Legend edwin sodi"
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_create_post(self):
        self.client.force_authenticate(self.user)

        response = self.client.post(
            self.posts_url,
            {
                "title": "My first post",
                "body": "Legend edwin sodi"
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "My first post")
        self.assertEqual(response.data["author"], "testuser")

    def test_post_author_is_assigned_by_the_server(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            self.posts_url,
            {
                "title": "Unauthenticated post",
                "body": "this shouldn't work",
                "author": self.other_user.username,
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['author'], "testuser")

    def test_posts_use_select_related_for_author(self):
        Post.objects.create(
            title="Second post",
            body="Another post.",
            author=self.user,
        )

        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(self.posts_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(f"\nNumber of database queries: {len(queries)}")

    def test_author_can_update_own_post(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.patch(
            self.detail_url,
             {"title": "Updated title"},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, "Updated title")


    def test_other_user_cannot_update_post(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.patch(
            self.detail_url,
            {"title": "Someone else's title",},
            format="json"
        )
        print("RESPONSE : ", response.data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, "My original post")

    def test_other_user_cannot_delete_post(self):
        self.client.force_authenticate(user=self.other_user)

        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Post.objects.filter(id=self.post.id).exists())

    def test_author_can_delete_own_post(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())


