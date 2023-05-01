from rest_framework.test import APITestCase
from .models import User


# urlpatterns = [
#     path("me/", views.Me.as_view()),
#     path("me/feedlike/", views.FeedLikes.as_view()),
#     # path("me/commentlike/", views.CommentLikes.as_view()),
#     path("me/feedlist/", views.FeedList.as_view()),
#     path("me/commentlist/", views.CommentList.as_view()),
#     # path("me/likelist/", views.LikeList.as_view()),
#     # path("@<str:username>/", views.UserDetail.as_view()),
#     path("login/", views.LogIn.as_view()),
#     path("logout/", views.LogOut.as_view()),
#     path("checkID/", views.CheckID.as_view()),
#     path("signup/", views.SignUp.as_view()),
#     path("signup/coach", views.CoachSignUp.as_view()),
#     path("find/id/", views.FindId.as_view()),
#     path("find/password/", views.FindPassword.as_view()),
#     path("changepassword/", views.ChangePassword.as_view()),
#     path("new-password/", views.NewPassword.as_view()),
#     # path("refresh/", TokenRefreshView.as_view()),
# ]
class SelfUsersView(APITestCase):
    URL = "/api/v1/users/me/"

    @classmethod
    def setUpTestData(cls) -> None:
        print("")
        print("Test View my Profile GET / PUT")
        cls.user = User.objects.create(username="TestUser")

    def test_view_user_profile_non_login(self):
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, 403, "Non Login User")

    def test_view_user_profile_login_user(self):
        self.client.force_login(self.user)
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, 200, "Login User")
        self.assertEqual(response.data.get("id"), self.user.id, "Self user profile")

    def test_edit_user_profile_non_user(self):
        response = self.client.put(self.URL)
        self.assertEqual(response.status_code, 403, "Non Login User")

    def test_view_user_profile_login_user(self):
        self.client.force_login(self.user)
        response = self.client.put(self.URL, {"username": "TestEdit"})
        self.assertEqual(response.status_code, 200, "Login User Edit")
        self.assertNotEqual(
            self.user.username, User.objects.get(pk=1).username, "Edit Profile check"
        )


# class SelfUsersView(APITestCase):
#     URL = "/api/v1/users/me/feedlike/"

#     @classmethod
#     def setUpTestData(cls) -> None:
#         print("")
#         print("Test View my liked feed GET")
#         cls.user = User.objects.create(username="TestUser")

#     def test_view_user_profile_non_login(self):
#         response = self.client.get(self.URL)
#         self.assertEqual(response.status_code, 403, "Non Login User")

#     def test_view_user_profile_login_user(self):
#         self.client.force_login(self.user)
#         response = self.client.get(self.URL)
#         self.assertEqual(response.status_code, 200, "Login User")
#         self.assertEqual(response.data.get("id"), self.user.id, "Self user profile")
