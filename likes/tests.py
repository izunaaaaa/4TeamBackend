from rest_framework.test import APITestCase
from users.models import User
from likes.models import Feedlike, Commentlike
from feeds.models import Feed
from groups.models import Group
from categories.models import Category
from accessinfo.models import AccessInfo
from comments.models import Comment, Recomment


# Create your tests here.
class FeedLikeView(APITestCase):
    URL = "/api/v1/likes/feedlike/1"

    @classmethod
    def setUpTestData(cls) -> None:
        print("")
        print("Test Created / delete my liked feed POST")
        cls.user = User.objects.create(username="TestUser")
        cls.group = Group.objects.create(name="Testgroup")
        cls.category = Category.objects.create(name="TestCategory", group=cls.group)
        cls.feed = Feed.objects.create(
            user=cls.user,
            group=cls.group,
            category=cls.category,
            title="Test Title",
        )
        cls.liked_feed = Feedlike.objects.create(feed=cls.feed, user=cls.user)

    def test_create_user_liked_feed_list_non_login(self):
        response = self.client.post(self.URL)
        self.assertEqual(response.status_code, 403, "Non Login User")

    def test_create_user_liked_feed_list_login(self):
        self.client.force_login(self.user)
        response = self.client.post(self.URL)
        self.assertEqual(response.status_code, 200, "Login User")
        self.assertEqual(
            Feedlike.objects.filter(user=self.user).count(),
            0,
            "Delete Feed like",
        )
        response = self.client.post(self.URL)
        self.assertEqual(
            Feedlike.objects.filter(user=self.user).count(),
            1,
            "Create Feed Like",
        )


class CommentLikeView(APITestCase):
    URL = "/api/v1/likes/commentlike/1"

    @classmethod
    def setUpTestData(cls) -> None:
        print("")
        print("Test Created / delete my liked Comment POST")
        cls.user = User.objects.create(username="TestUser")
        cls.group = Group.objects.create(name="Testgroup")
        cls.category = Category.objects.create(name="TestCategory", group=cls.group)
        cls.feed = Feed.objects.create(
            user=cls.user,
            group=cls.group,
            category=cls.category,
            title="Test Title",
        )
        cls.comment = Comment.objects.create(feed=cls.feed, user=cls.user)

    def test_create_user_liked_comment_list_non_login(self):
        response = self.client.post(self.URL)
        self.assertEqual(response.status_code, 403, "Non Login User")

    def test_create_user_liked_comment_list_login(self):
        self.client.force_login(self.user)
        response = self.client.post(self.URL)
        self.assertEqual(response.status_code, 200, "Login User")
        self.assertEqual(
            Commentlike.objects.filter(user=self.user).count(),
            1,
            "create comment like",
        )
        response = self.client.post(self.URL)
        self.assertEqual(
            Feedlike.objects.filter(user=self.user).count(),
            0,
            "delete comment Like",
        )


class CommentLikeView(APITestCase):
    URL = "/api/v1/likes/recommentlike/1"

    @classmethod
    def setUpTestData(cls) -> None:
        print("")
        print("Test Created / delete my liked Recomment POST")
        cls.user = User.objects.create(username="TestUser")
        cls.group = Group.objects.create(name="Testgroup")
        cls.category = Category.objects.create(name="TestCategory", group=cls.group)
        cls.feed = Feed.objects.create(
            user=cls.user,
            group=cls.group,
            category=cls.category,
            title="Test Title",
        )
        cls.comment = Comment.objects.create(feed=cls.feed, user=cls.user)
        cls.recomment = Recomment.objects.create(comment=cls.comment, user=cls.user)

    def test_create_user_liked_recomment_list_non_login(self):
        response = self.client.post(self.URL)
        self.assertEqual(response.status_code, 403, "Non Login User")

    def test_create_user_liked_recomment_list_login(self):
        self.client.force_login(self.user)
        response = self.client.post(self.URL)
        self.assertEqual(response.status_code, 200, "Login User")
        self.assertEqual(
            Commentlike.objects.filter(user=self.user).count(),
            1,
            "create comment like",
        )
        response = self.client.post(self.URL)
        self.assertEqual(
            Feedlike.objects.filter(user=self.user).count(),
            0,
            "delete comment Like",
        )
