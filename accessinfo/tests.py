from rest_framework.test import APITestCase
from users.models import User
from groups.models import Group
from .models import AccessInfo


class AccessInfoAll(APITestCase):
    URL = "/api/v1/access/"

    @classmethod
    def setUpTestData(cls):
        print("Access Info POST")
        cls.test_user = User.objects.create(
            username="testuser", email="art970@naver.com"
        )
        cls.test_user_coach = User.objects.create(
            username="testCoach", email="kdh97048@gmail.com", is_coach=True
        )

    def test_create_access_info_non_login_user(self):
        response = self.client.post(self.URL)
        self.assertEqual(response.status_code, 403, "Not logged in")

    def test_create_access_info_login_normal_user(self):
        self.client.force_login(self.test_user)
        response = self.client.post(self.URL)
        self.assertEqual(response.status_code, 403, "Not Coach")
        self.client.logout()

    def test_create_access_info_login_coach_user(self):
        import json

        self.client.force_login(self.test_user_coach)
        with open(
            "./post_test/access/new_post_example.json", "r", encoding="UTF-8"
        ) as json_data:
            data = json.load(json_data)

        data = json.dumps(data)
        response = self.client.post(
            self.URL,
            data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200, "Add data")

        group = Group.objects.count()
        self.assertEqual(group, 1, "Add group")
        group = Group.objects.get(pk=1)
        self.assertEqual(group.categories.count(), 2, "Add category when create group")
        self.assertNotEqual(AccessInfo.objects.count(), 0, "Access User Post")

        self.client.logout()
