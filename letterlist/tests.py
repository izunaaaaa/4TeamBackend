from rest_framework.test import APITestCase
from users.models import User
from .models import Letter, Letterlist


class MyLetterlistView(APITestCase):
    URL = "/api/v1/letterlist/me/"

    @classmethod
    def setUpTestData(cls) -> None:
        print("")
        print("Test View my Letterlist GET")
        cls.user = User.objects.create(username="TestUser", email="Test@test.com")
        cls.user2 = User.objects.create(
            username="TestUser2", email="TestEmail@test.com"
        )
        cls.user3 = User.objects.create(username="TestUser3", email="Test3@test.com")
        cls.letter_list = Letterlist.objects.create()
        cls.letter_list.user.add(cls.user)
        cls.letter_list.user.add(cls.user2)

    def test_view_my_letter_list_non_login(self):
        res = self.client.get(self.URL)
        self.assertEqual(res.status_code, 403, "Non Login")

    def test_view_my_letter_list_login(self):
        self.client.force_login(self.user)
        res = self.client.get(self.URL)
        self.assertEqual(res.status_code, 200, "Login")
        self.assertEqual(len(res.data), 1, "Contain Letterlist")
        self.client.logout()

    def test_view_my_letter_list_login_other_user(self):
        self.client.force_login(self.user2)
        res = self.client.get(self.URL)
        self.assertEqual(res.status_code, 200, "Login")
        self.assertEqual(len(res.data), 1, "Contain Letterlist")
        self.client.logout()

    def test_view_my_letter_list_login_other_user_not_contain(self):
        self.client.force_login(self.user3)
        res = self.client.get(self.URL)
        self.assertEqual(res.status_code, 200, "Login")
        self.assertEqual(len(res.data), 0, "Contain Letterlist")
        self.client.logout()


class LetterView(APITestCase):
    URL = "/api/v1/letterlist/1/"

    @classmethod
    def setUpTestData(cls) -> None:
        print("")
        print("Test View my Letterlist GET / DELETE")
        cls.user = User.objects.create(username="TestUser", email="Test@test.com")
        cls.user2 = User.objects.create(
            username="TestUser2", email="TestEmail@test.com"
        )
        cls.user3 = User.objects.create(username="TestUser3", email="Test3@test.com")
        cls.letter_list = Letterlist.objects.create()
        cls.letter_list.user.add(cls.user)
        cls.letter_list.user.add(cls.user2)
        for i in range(5):
            Letter.objects.create(
                sender=cls.user if i % 2 == 0 else cls.user2,
                room=cls.letter_list,
            )

    def test_view_letter_list_non_login(self):
        res = self.client.get(self.URL)
        self.assertEqual(res.status_code, 403, "Non Login")

    def test_view_letter_list_login(self):
        self.client.force_login(self.user)
        res = self.client.get(self.URL)
        self.assertEqual(res.status_code, 200, "Login")
        self.assertEqual(len(res.data), 5, "Login")
        self.client.logout()

    def test_view_letter_list_login_other_user(self):
        self.client.force_login(self.user2)
        res = self.client.get(self.URL)
        self.assertEqual(res.status_code, 200, "Login other user")
        self.assertEqual(len(res.data), 5, "Login other user")
        self.client.logout()

    def test_view_letter_list_login_other_user_not_contain(self):
        self.client.force_login(self.user3)
        res = self.client.get(self.URL)
        self.assertEqual(res.status_code, 403, "Not contain")
        self.client.logout()

    def test_delete_letter_list_login_user_only_self(self):
        self.client.force_login(self.user)
        res = self.client.get("/api/v1/letterlist/me/")
        self.assertEqual(len(res.data), 1, "Check delete")

        res = self.client.delete(self.URL)
        self.assertEqual(res.status_code, 204, "Delete only self")

        res = self.client.get("/api/v1/letterlist/me/")
        self.assertEqual(len(res.data), 0, "Check delete")

        self.client.logout()

        self.client.force_login(self.user2)
        res = self.client.get("/api/v1/letterlist/me/")
        self.assertEqual(len(res.data), 1, "Check delete only self")

        self.client.logout()


class LetterSend(APITestCase):
    URL = "/api/v1/letterlist/message/"

    @classmethod
    def setUpTestData(cls) -> None:
        print("")
        print("Test create Letter POST")
        cls.user = User.objects.create(username="TestUser", email="Test@test.com")
        cls.user2 = User.objects.create(
            username="TestUser2", email="TestEmail@test.com"
        )

    def test_craete_message_non_login(self):
        res = self.client.post(self.URL)
        self.assertEqual(res.status_code, 403, "Non Login")

    def test_craete_message_login_not_message(self):
        self.client.force_login(self.user)
        res = self.client.post(self.URL, {"receiver": 2})
        self.assertEqual(res.status_code, 400, "Not Message")
        self.client.logout()

    def test_craete_message_login_not_receiver(self):
        self.client.force_login(self.user)
        res = self.client.post(self.URL, {"text": "TEST"})
        self.assertEqual(res.status_code, 400, "Not receiver")
        self.client.logout()

    def test_craete_message_login_successfully(self):
        self.client.force_login(self.user)
        res = self.client.post(self.URL, {"receiver": 2, "text": "TEST"})
        self.assertEqual(res.status_code, 201, "Successfully Case")
        self.client.logout()

    def test_craete_message_login_send_myself(self):
        self.client.force_login(self.user)
        res = self.client.post(self.URL, {"receiver": 1, "text": "TEST"})
        self.assertEqual(res.status_code, 400, "Cannot Send self")
        self.client.logout()

    def test_craete_message_login_check_make_letterlist(self):
        self.client.force_login(self.user)
        before = Letterlist.objects.count()
        res = self.client.post(self.URL, {"receiver": 2, "text": "TEST"})
        after = Letterlist.objects.count()
        self.assertNotEqual(before, after, "Check Make LetterList")


class LetterSend(APITestCase):
    URL = "/api/v1/letterlist/message/1/"

    @classmethod
    def setUpTestData(cls) -> None:
        print("")
        print("Test Delete Letter DELETE")
        cls.user = User.objects.create(username="TestUser", email="Test@test.com")
        cls.user2 = User.objects.create(
            username="TestUser2", email="TestEmail@test.com"
        )
        cls.user3 = User.objects.create(
            username="TestUser3", email="TestEmail3@test.com"
        )
        cls.letter_list = Letterlist.objects.create()
        cls.letter_list.user.add(cls.user)
        cls.letter_list.user.add(cls.user2)
        for i in range(5):
            Letter.objects.create(
                sender=cls.user if i % 2 == 0 else cls.user2,
                room=cls.letter_list,
            )

    def test_delete_letter_non_login(self):
        res = self.client.delete(self.URL)
        self.assertEqual(res.status_code, 403, "Not Logged in")

    def test_delete_letter_login(self):
        self.client.force_login(self.user)

        before = len(self.client.get("/api/v1/letterlist/1/").data)
        res = self.client.delete(self.URL)

        self.assertEqual(res.status_code, 204, "Logged in")
        after = len(self.client.get("/api/v1/letterlist/1/").data)
        self.assertNotEqual(before, after, "Delete Check")

        self.client.logout()

        self.client.force_login(self.user2)

        other_user_letter = len(self.client.get("/api/v1/letterlist/1/").data)

        self.assertEqual(before, other_user_letter, "Delete Check only self")

    def test_delete_letter_other_user(self):
        self.client.force_login(self.user3)
        res = self.client.delete(self.URL)
        self.assertEqual(res.status_code, 403, "Cannot delete Other user")

    def test_delete_letter_access_does_not_exist_resource(self):
        self.client.force_login(self.user3)
        res = self.client.delete("/api/v1/letterlist/message/6/")
        self.assertEqual(res.status_code, 404, "Cannot Access This URL")
