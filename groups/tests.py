from rest_framework.test import APITestCase
from users.models import User
from .models import Group


class AllGroupTestCase(APITestCase):
    URL = "/api/v1/groups/"

    @classmethod
    def setUpTestData(cls):
        print("")
        print("All Group Info GET")
        cls.group = Group.objects.create(name="testGroup")
        cls.group2 = Group.objects.create(name="testGroup2")

    def test_view_all_groups(self):
        response = self.client.get(self.URL)
        data = response.json()
        self.assertEqual(response.status_code, 200, "status isn't 200")
        # self.assertEqual(len(data), 2, "Show all groups")


class GroupDetailTestCase(APITestCase):
    URL = "/api/v1/groups/1"

    @classmethod
    def setUpTestData(cls) -> None:
        print("")
        print("Group Detail GET PUT DELETE")
        cls.group = Group.objects.create(name="testGroup")
        cls.group2 = Group.objects.create(name="testGroup2")
        cls.user = User.objects.create(
            username="testUser",
            email="testEmail@email.com",
        )
        cls.coach_user = User.objects.create(
            username="testUser2",
            group=cls.group,
            email="testEmail2@email.com",
        )
        cls.other_coach_user = User.objects.create(
            username="testUser3",
            group=cls.group2,
            email="testEmail3@email.com",
        )

    def test_view_group_detail(self):
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, 200, "status isn't 200")
        self.assertEqual(response.data.get("name"), "testGroup")

    def test_view_group_detail_dont_exist_url(self):
        response = self.client.get("/api/v1/groups/3")
        self.assertEqual(response.status_code, 404, "does not exist")

    def test_edit_group_detail_non_login(self):
        response = self.client.put(self.URL, {"name": "test"})
        self.assertEqual(response.status_code, 403, "Permission denied")

    def test_edit_group_detail_normal_login(self):
        self.client.force_login(self.user)

        response = self.client.put(self.URL, {"name": "test"})
        self.assertEqual(response.status_code, 403, "Permission denied")

        self.client.logout()

    def test_edit_group_detail_coach_login(self):
        self.client.force_login(self.coach_user)

        response = self.client.put(self.URL, {"name": "test"})
        self.assertEqual(response.status_code, 200, "Success Access")
        self.assertNotEqual(Group.objects.get(pk=1).name, "testGroup", "check change")
        self.assertEqual(Group.objects.get(pk=1).name, "test", "check change")

        self.client.logout()

    def test_edit_group_detail_other_coach_login(self):
        self.client.force_login(self.other_coach_user)

        response = self.client.put(self.URL, {"name": "test"})
        self.assertEqual(response.status_code, 403, "Permission denied")

        self.client.logout()

    def test_delete_group_detail_non_login_user(self):
        response = self.client.delete(self.URL)
