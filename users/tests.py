from rest_framework.test import APITestCase
from .models import User
from likes.models import Feedlike
from feeds.models import Feed
from groups.models import Group
from categories.models import Category
from accessinfo.models import AccessInfo


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


class SelfUsersFeedLikeView(APITestCase):
    URL = "/api/v1/users/me/feedlike/"

    @classmethod
    def setUpTestData(cls) -> None:
        print("")
        print("Test View my liked feed GET / POST")
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

    def test_view_user_liked_feed_list_non_login(self):
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, 403, "Non Login User")

    def test_view_user_liked_feed_list_login(self):
        self.client.force_login(self.user)
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, 200, "Login User")
        self.assertEqual(
            response.data.get("count"),
            Feedlike.objects.filter(user=self.user).count(),
            "Self user Feed list",
        )

    def test_create_user_liked_feed_list_non_login(self):
        response = self.client.post(self.URL)
        self.assertEqual(response.status_code, 403, "Non Login User")

    def test_create_user_liked_feed_list_login(self):
        self.client.force_login(self.user)
        response = self.client.post(self.URL, {"feed": 1})
        self.assertEqual(response.status_code, 200, "Login User")
        self.assertEqual(
            Feedlike.objects.filter(user=self.user).count(),
            0,
            "Delete Feed like",
        )
        Feed.objects.create(
            user=self.user,
            group=self.group,
            category=self.category,
            title="Test Title2",
        )
        response = self.client.post(self.URL, {"feed": 2})
        self.assertEqual(
            Feedlike.objects.filter(user=self.user).count(),
            1,
            "Create Feed Like",
        )


class SelfUsersFeedListView(APITestCase):
    URL = "/api/v1/users/me/feedlist/"

    @classmethod
    def setUpTestData(cls) -> None:
        print("")
        print("Test View my liked feed GET / POST")
        cls.user = User.objects.create(username="TestUser")
        cls.group = Group.objects.create(name="Testgroup")
        cls.category = Category.objects.create(name="TestCategory", group=cls.group)
        cls.feed = Feed.objects.create(
            user=cls.user,
            group=cls.group,
            category=cls.category,
            title="Test Title",
        )

    def test_view_user_liked_feed_list_non_login(self):
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, 403, "Non Login User")

    def test_view_user_liked_feed_list_login(self):
        self.client.force_login(self.user)
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, 200, "Login User")
        self.assertEqual(
            response.data.get("count"),
            Feed.objects.filter(user=self.user).count(),
            "Self user Feed list",
        )


class TestLogin(APITestCase):
    URL = "/api/v1/users/login/"

    @classmethod
    def setUpTestData(cls) -> None:
        print("")
        print("Test Login POST")
        user = User.objects.create(username="TestUser")
        user.set_password("TestPassword")
        user.save()

    def test_login(self):
        response = self.client.post(
            self.URL,
            data={
                "username": "TestUser",
                "password": "TestPassword",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 200, "정상적인 로그인")

    def test_login_diff_password(self):
        response = self.client.post(
            self.URL,
            data={
                "username": "TestUser",
                "password": "Error Password",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400, "잘못된 비밀번호")

    def test_login_diff_username(self):
        response = self.client.post(
            self.URL,
            data={
                "username": "ErrorUser",
                "password": "Test Password",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400, "잘못된 아이디")


class TestSignUpNormalUser(APITestCase):
    URL = "/api/v1/users/signup/"

    @classmethod
    def setUpTestData(cls) -> None:
        print("")
        print("Test Signup Normal User POST")
        cls.group = Group.objects.create(name="Test Group")
        cls.access_info = AccessInfo.objects.create(
            name="Test",
            phone_number="01011148077",
            email="art970@naver.com",
            group=cls.group,
        )

    def test_create_sign_up(self):
        response = self.client.post(
            self.URL,
            data={
                "username": "Test",
                "password": "TestPassword1!",
                "phone_number": "01011148077",
                "email": "art970@naver.com",
                "name": "Test",
                "group": self.group.pk,
                "gender": "male",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201, "정상적인 경우")
        self.assertNotEqual(
            self.access_info.is_signup,
            AccessInfo.objects.get(pk=1).is_signup,
            "Is Sign up 변경",
        )

    def test_create_sign_up_not_valid_password(self):
        response = self.client.post(
            self.URL,
            data={
                "username": "Test",
                "password": "1",
                "phone_number": "01011148077",
                "email": "art970@naver.com",
                "name": "Test",
                "group": self.group.pk,
                "gender": "male",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400, "비밀번호 유효성 검사 실패")

    def test_create_sign_up_does_not_exist_in_access_info(self):
        response = self.client.post(
            self.URL,
            data={
                "username": "Test",
                "password": "TestPassword1!",
                "phone_number": "01011148077",
                "email": "art970@naver.com",
                "name": "Test_not_in_access_info",
                "group": self.group.pk,
                "gender": "male",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 403, "Access 모델에 존재하지 않는 경우")

    def test_create_sign_up_does_not_exist_password(self):
        response = self.client.post(
            self.URL,
            data={
                "username": "Test",
                "phone_number": "01011148077",
                "email": "art970@naver.com",
                "name": "Test",
                "group": self.group.pk,
                "gender": "male",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400, "Password 가 존재하지 않는 경우")

    def test_create_sign_up_does_not_exist_group(self):
        response = self.client.post(
            self.URL,
            data={
                "username": "Test",
                "phone_number": "01011148077",
                "password": "TestPassword1!",
                "email": "art970@naver.com",
                "name": "Test",
                "gender": "male",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 404, "Group 이 존재하지 않는 경우")


class TestSignUpCoachUser(APITestCase):
    URL = "/api/v1/users/signup/coach"

    @classmethod
    def setUpTestData(cls) -> None:
        print("")
        print("Test Signup Coach POST")
        cls.group = Group.objects.create(name="Test Group")
        cls.access_info = AccessInfo.objects.create(
            name="Test",
            phone_number="01011148077",
            email="art970@naver.com",
            group=cls.group,
        )

    def test_create_sign_up_coach_create_group(self):
        response = self.client.post(
            self.URL,
            data={
                "username": "Test",
                "password": "TestPassword1!",
                "phone_number": "01011148077",
                "email": "art970@naver.com",
                "name": "Test",
                "group": "NewGroup",
                "gender": "male",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201, "정상적인 경우 ( 그룹 생성 )")
        self.assertEqual(Group.objects.count(), 2, "그룹 생성 여부 테스트")

    def test_create_sign_up_coach_not_create_group(self):
        response = self.client.post(
            self.URL,
            data={
                "username": "Test",
                "password": "TestPassword1!",
                "phone_number": "01011148077",
                "email": "art970@naver.com",
                "name": "Test",
                "group": "Test Group",
                "gender": "male",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201, "정상적인 경우 ( 이미 있는 그룹 )")
        self.assertEqual(Group.objects.count(), 1, "그룹 생성 여부 테스트")


class TestFindId(APITestCase):
    URL = "/api/v1/users/find/id/"

    @classmethod
    def setUpTestData(cls) -> None:
        print("")
        print("Test Find Id POST")
        cls.user = User.objects.create(
            username="TestUser",
            name="Test",
            email="test@example.com",
            phone_number="01000000000",
        )

    def test_view_find_id(self):
        response = self.client.post(
            self.URL,
            data={
                "name": "Test",
                "phone_number": "01000000000",
                "email": "test@example.com",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 200, "아이디 찾기")
        self.assertEqual(response.data.get("id"), "TestUser", "아이디 찾기 결과")

    def test_view_find_id_non_name(self):
        response = self.client.post(
            self.URL,
            data={
                "phone_number": "01000000000",
                "email": "test@example.com",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400, "아이디 찾기 (이름 없는 경우)")

    def test_view_find_id_non_phone_number(self):
        response = self.client.post(
            self.URL,
            data={
                "phone_number": "01000000000",
                "email": "test@example.com",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400, "아이디 찾기 ( 비밀번호 없는 경우 )")

    def test_view_find_id_non_email(self):
        response = self.client.post(
            self.URL,
            data={
                "name": "Test",
                "phone_number": "01000000000",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400, "아이디 찾기 ( 이메일 없는 경우 )")

    def test_view_find_id_does_not_user(self):
        response = self.client.post(
            self.URL,
            data={
                "name": "Test1",
                "phone_number": "01000000010",
                "email": "test@example.co",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 404, "아이디 찾기 실패")


class TestFindPassword(APITestCase):
    URL = "/api/v1/users/find/password/"

    @classmethod
    def setUpTestData(cls) -> None:
        print("")
        print("Test find password POST")
        cls.user = User.objects.create(
            username="TestUser",
            name="Test",
            email="test@example.com",
            phone_number="01000000000",
        )

    def test_view_find_password(self):
        response = self.client.post(
            self.URL,
            data={
                "username": "TestUser",
                "name": "Test",
                "phone_number": "01000000000",
                "email": "test@example.com",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 200, "비밀번호 찾기")

    def test_view_find_password_non_name(self):
        response = self.client.post(
            self.URL,
            data={
                "username": "TestUser",
                "phone_number": "01000000000",
                "email": "test@example.com",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400, "비밀번호 찾기 (이름 없는 경우)")

    def test_view_find_password_non_phone_number(self):
        response = self.client.post(
            self.URL,
            data={
                "username": "TestUser",
                "phone_number": "01000000000",
                "email": "test@example.com",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400, "비밀번호 찾기 ( 비밀번호 없는 경우 )")

    def test_view_find_password_non_email(self):
        response = self.client.post(
            self.URL,
            data={
                "username": "TestUser",
                "name": "Test",
                "phone_number": "01000000000",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400, "비밀번호 찾기 ( 이메일 없는 경우 )")

    def test_view_find_password_does_not_exist_user(self):
        response = self.client.post(
            self.URL,
            data={
                "username": "TestUser",
                "name": "Test1",
                "phone_number": "01000000010",
                "email": "test@example.co",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 404, "아이디 찾기 실패")


class TestFindPassword(APITestCase):
    URL = "/api/v1/users/changepassword/"

    @classmethod
    def setUpTestData(cls) -> None:
        print("")
        print("Test change password PUT")
        cls.user = User.objects.create(
            username="TestUser",
            name="Test",
            email="test@example.com",
            phone_number="01000000000",
        )
        cls.password = "Testpassword"
        cls.user.set_password(cls.password)
        cls.user.save()

    def test_change_password_non_login_user(self):
        response = self.client.put(
            self.URL,
            data={
                "old_password": self.password,
                "new_password": "NewPassword",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 403, "비밀번호 변경 실패")

    def test_change_password_invalid_password(self):
        self.client.force_login(self.user)
        response = self.client.put(
            self.URL,
            data={
                "old_password": self.password,
                "new_password": "NewPassword",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400, "비밀번호 변경 ( 유효성 실패 )")
        self.client.logout()

    def test_change_password_invalid_password(self):
        self.client.force_login(self.user)
        response = self.client.put(
            self.URL,
            data={
                "old_password": self.password,
                "new_password": "NewPassword111!",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 200, "비밀번호 변경 ( 유효성 실패 )")
        self.client.logout()

    def test_change_password_wrong_password(self):
        self.client.force_login(self.user)
        response = self.client.put(
            self.URL,
            data={
                "old_password": "Wrong Old Password",
                "new_password": "NewPassword",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400, "비밀번호 변경 실패")
        self.client.logout()

    def test_change_password_invalid_value(self):
        self.client.force_login(self.user)
        response = self.client.put(
            self.URL,
            data={
                "new_password": "NewPassword",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400, "비밀번호 변경 실패")
        response = self.client.put(
            self.URL,
            data={
                "old_password": self.password,
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400, "비밀번호 변경 실패")
        self.client.logout()


class TestChangeNewPassword(APITestCase):
    URL = "/api/v1/users/new-password/"

    @classmethod
    def setUpTestData(cls) -> None:
        print("")
        print("Test find password POST")
        cls.user = User.objects.create(
            username="TestUser",
            name="Test",
            email="test@example.com",
            phone_number="01000000000",
        )

    def test_view_find_password(self):
        response = self.client.put(
            self.URL,
            data={
                "username": "TestUser",
                "name": "Test",
                "phone_number": "01000000000",
                "email": "test@example.com",
                "password": "pa11ssword1!",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 200, "비밀번호 변경")

    def test_view_find_password_non_name(self):
        response = self.client.put(
            self.URL,
            data={
                "username": "TestUser",
                "phone_number": "01000000000",
                "email": "test@example.com",
                "password": "pa11ssword1!",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400, "비밀번호 찾기 (이름 없는 경우)")

    def test_view_find_password_non_phone_number(self):
        response = self.client.put(
            self.URL,
            data={
                "username": "TestUser",
                "phone_number": "01000000000",
                "email": "test@example.com",
                "password": "pa11ssword1!",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400, "비밀번호 변경 ( 비밀번호 없는 경우 )")

    def test_view_find_password_non_email(self):
        response = self.client.put(
            self.URL,
            data={
                "username": "TestUser",
                "name": "Test",
                "phone_number": "01000000000",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400, "비밀번호 변경 ( 이메일 없는 경우 )")

    def test_view_find_password_does_not_exist_user(self):
        response = self.client.put(
            self.URL,
            data={
                "username": "TestUser",
                "name": "Test1",
                "phone_number": "01000000010",
                "email": "test@example.co",
                "password": "pa11ssword1!",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 404, "비밀번호 변경 실패")
