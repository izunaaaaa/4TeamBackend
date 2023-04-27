from rest_framework.test import APITestCase
from .models import Comment, Recomment
from users.models import User
from groups.models import Group
from feeds.models import Feed
from categories.models import Category


class CommentDelete(APITestCase):
    URL = "/api/v1/comments/1"

    @classmethod
    def setUpTestData(self):
        print("")
        print("Comment DELETE")
        self.group = Group.objects.create(name="TestGroup")
        self.category = Category.objects.create(name="TestCategory", group=self.group)
        self.user = User.objects.create(
            username="TestUser",
            group=self.group,
            email="TestUser@Test.com",
        )
        self.other_user = User.objects.create(
            username="TestUser2",
            group=self.group,
            email="TestUser2@Test.com",
        )
        self.coach = User.objects.create(
            username="TestCoach",
            group=self.group,
            email="TestCoach@Test.com",
            is_coach=True,
        )
        self.feed = Feed.objects.create(
            user=self.user,
            title="TestTitle",
            category=self.category,
        )
        Comment.objects.create(
            description="TestComment", user=self.user, feed=self.feed
        )
        Comment.objects.create(
            description="TestComment2", user=self.other_user, feed=self.feed
        )

    def test_delete_comment_non_login_user(self):
        response = self.client.delete(self.URL)
        self.assertEqual(response.status_code, 403, "Non Login User")

    def test_delete_comment_login_user_writer(self):
        self.client.force_login(self.user)
        response = self.client.delete(self.URL)
        self.assertEqual(response.status_code, 204, "Login User (writer)")
        self.client.logout()

    def test_delete_comment_login_user_not_writer(self):
        self.client.force_login(self.other_user)
        response = self.client.delete(self.URL)
        self.assertEqual(response.status_code, 403, "Login User (Not writer)")
        self.client.logout()

    def test_delete_comment_login_user_not_writer_but_coach(self):
        self.client.force_login(self.coach)
        response = self.client.delete(self.URL)
        self.assertEqual(response.status_code, 204, "Login User (coach)")
        self.client.logout()

    def test_delete_comment_real_delete_check(self):
        self.client.force_login(self.coach)
        before = Comment.objects.count()
        response = self.client.delete(self.URL)
        after = Comment.objects.count()
        self.assertNotEqual(before, after, "Delete Check")
        self.client.logout()

    def test_delete_comment_not_exist_url(self):
        self.client.force_login(self.coach)
        response = self.client.delete("/api/v1/comments/3")
        self.assertEqual(response.status_code, 404, "does not exist pk")
        self.client.logout()


class CommentTest(APITestCase):
    URL = "/api/v1/comments/recomments/1"

    @classmethod
    def setUpTestData(self):
        print("")
        print("ReComment DELETE")
        self.group = Group.objects.create(name="TestGroup")
        self.category = Category.objects.create(name="TestCategory", group=self.group)
        self.user = User.objects.create(
            username="TestUser",
            group=self.group,
            email="TestUser@Test.com",
        )
        self.other_user = User.objects.create(
            username="TestUser2",
            group=self.group,
            email="TestUser2@Test.com",
        )
        self.coach = User.objects.create(
            username="TestCoach",
            group=self.group,
            email="TestCoach@Test.com",
            is_coach=True,
        )
        self.feed = Feed.objects.create(
            user=self.user,
            title="TestTitle",
            category=self.category,
        )
        self.comment = Comment.objects.create(
            description="TestComment",
            user=self.user,
            feed=self.feed,
        )
        Recomment.objects.create(
            description="TestComment1",
            user=self.user,
            comment=self.comment,
        )
        Recomment.objects.create(
            description="TestComment2",
            user=self.other_user,
            comment=self.comment,
        )

    def test_delete_comment_non_login_user(self):
        response = self.client.delete(self.URL)
        self.assertEqual(response.status_code, 403, "Non Login User")

    def test_delete_comment_login_user_writer(self):
        self.client.force_login(self.user)
        response = self.client.delete(self.URL)
        self.assertEqual(response.status_code, 204, "Login User (writer)")
        self.client.logout()

    def test_delete_comment_login_user_not_writer(self):
        self.client.force_login(self.other_user)
        response = self.client.delete(self.URL)
        self.assertEqual(response.status_code, 403, "Login User (Not writer)")
        self.client.logout()

    def test_delete_comment_login_user_not_writer_but_coach(self):
        self.client.force_login(self.coach)
        response = self.client.delete(self.URL)
        self.assertEqual(response.status_code, 204, "Login User (coach)")
        self.client.logout()

    def test_delete_comment_real_delete_check(self):
        self.client.force_login(self.coach)
        before = Recomment.objects.count()
        self.client.delete(self.URL)
        after = Recomment.objects.count()
        self.assertNotEqual(before, after, "Delete Check")
        self.client.logout()

    def test_delete_comment_not_exist_url(self):
        self.client.force_login(self.coach)
        response = self.client.delete("/api/v1/comments/recomment/3")
        self.assertEqual(response.status_code, 404, "does not exist pk")
        self.client.logout()
