from rest_framework.test import APITestCase
from users.models import User
from groups.models import Group
from .models import AccessInfo
import json


class AccessInfoAll(APITestCase):
    URL = "/api/v1/access/"

    @classmethod
    def setUpTestData(cls):
        print("")
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

    def test_create_access_info_login_coach_user_does_not_exist_group(self):
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
        for i in AccessInfo.objects.all():
            self.assertEqual(i.group, group, "Access User Group Check")
        self.client.logout()

    def test_create_access_info_login_coach_user_already_exis_group(self):
        self.client.force_login(self.test_user_coach)
        with open(
            "./post_test/access/new_post_example.json", "r", encoding="UTF-8"
        ) as json_data:
            first_data = json.load(json_data)
        with open(
            "./post_test/access/already_exist_group_post.json", "r", encoding="UTF-8"
        ) as json_data:
            second_data = json.load(json_data)
        first_data = json.dumps(first_data)
        second_data = json.dumps(second_data)
        response = self.client.post(
            self.URL,
            first_data,
            content_type="application/json",
        )
        first_data_count = AccessInfo.objects.count()
        response = self.client.post(
            self.URL,
            second_data,
            content_type="application/json",
        )
        group = Group.objects.count()
        self.assertEqual(group, 1, "already exist group")
        self.assertNotEqual(AccessInfo.objects.count(), first_data_count, "Add User")
        group = Group.objects.get(pk=1)
        for i in AccessInfo.objects.all():
            self.assertEqual(i.group, group, "Access User Group Check")
        self.client.logout()

    def test_create_access_info_error_value_non_field(self):
        self.client.force_login(self.test_user_coach)
        with open(
            "./post_test/access/error/non_field.json", "r", encoding="UTF-8"
        ) as json_data:
            data = json.load(json_data)
        data = json.dumps(data)
        response = self.client.post(
            self.URL,
            data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400, "non field data")
        group = Group.objects.count()
        self.assertEqual(group, 0, "Add Group failed")
        self.client.logout()

    def test_create_access_info_error_value_non_group(self):
        self.client.force_login(self.test_user_coach)
        with open(
            "./post_test/access/error/non_group.json", "r", encoding="UTF-8"
        ) as json_data:
            data = json.load(json_data)
        data = json.dumps(data)
        response = self.client.post(
            self.URL,
            data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400, "non field data")
        self.client.logout()

    def test_create_access_info_error_value_duplication_value(self):
        self.client.force_login(self.test_user_coach)
        with open(
            "./post_test/access/error/duplication_value.json", "r", encoding="UTF-8"
        ) as json_data:
            data = json.load(json_data)
        data = json.dumps(data)
        response = self.client.post(
            self.URL,
            data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400, "duplicate value data")
        group = Group.objects.count()
        self.assertEqual(group, 0, "Add group failed")


class AccessInfoGroup(APITestCase):
    URL = "/api/v1/access/group/1"

    @classmethod
    def setUpTestData(self):
        print("")
        print("Access Group Info GET / POST")
        self.group = Group.objects.create(name="TestGroup")
        self.other_group = Group.objects.create(name="TestGroup2")
        self.test_user = User.objects.create(
            username="testuser",
            email="art970@naver.com",
        )
        self.test_user_group_coach = User.objects.create(
            username="testCoach",
            email="kdh97048@gmail.com",
            is_coach=True,
            group=self.group,
        )
        self.test_user_other_coach = User.objects.create(
            username="testOtherCoach",
            email="kdh97049@gmail.com",
            is_coach=True,
            group=self.other_group,
        )
        with open(
            "./post_test/access/new_post_example.json", "r", encoding="UTF-8"
        ) as json_data:
            data = json.load(json_data)
        for i in data.get("members"):
            AccessInfo.objects.create(
                name=i.get("name"),
                email=i.get("email"),
                phone_number=i.get("phone_number"),
                group=self.group,
            )
        AccessInfo.objects.create(
            name="test",
            email="test@test.com",
            phone_number="01088848077",
            group=self.other_group,
        )

    def test_view_access_info_non_login_user(self):
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, 403, "Non login user")

    def test_view_access_info_login_normal_user(self):
        self.client.force_login(self.test_user)
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, 403, "login normal user")
        self.client.logout()

    def test_view_access_info_login_other_group_coach_user(self):
        self.client.force_login(self.test_user_other_coach)
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, 403, "login other coach user")
        self.client.logout()

    def test_view_access_info_login_group_coach_user(self):
        self.client.force_login(self.test_user_group_coach)
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, 200, "login coach user")
        self.assertNotEqual(
            len(response.data), AccessInfo.objects.count(), "Don't show all data"
        )
        self.client.logout()

    def test_view_access_info_login_other_coach_user(self):
        self.client.force_login(self.test_user_other_coach)
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, 403, "login other coach user")
        self.client.logout()

    def test_add_access_info_non_login_user(self):
        response = self.client.post(self.URL)
        self.assertEqual(response.status_code, 403, "Non login user")
        self.client.logout()

    def test_add_access_info_login_normal_user(self):
        self.client.force_login(self.test_user)
        response = self.client.post(self.URL)
        self.assertEqual(response.status_code, 403, "Not Coach user")
        self.client.logout()

    def test_add_access_info_login_other_coach_user(self):
        self.client.force_login(self.test_user_other_coach)
        response = self.client.post(self.URL)
        self.assertEqual(response.status_code, 403, "Other Group Coach user")
        self.client.logout()

    def test_add_access_info_login_coach_user(self):
        self.client.force_login(self.test_user_group_coach)
        check_count = AccessInfo.objects.count()
        with open(
            "./post_test/access/add_post_example.json", "r", encoding="UTF-8"
        ) as json_data:
            data = json.load(json_data)
        data = json.dumps(data)
        response = self.client.post(
            self.URL,
            data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200, "Group Coach user")
        self.assertNotEqual(AccessInfo.objects.count(), check_count, "Add check")
        self.client.logout()

    def test_add_access_info_login_coach_user_duplicated_value(self):
        self.client.force_login(self.test_user_group_coach)
        check_count = AccessInfo.objects.count()
        with open(
            "./post_test/access/error/add_post_example.json", "r", encoding="UTF-8"
        ) as json_data:
            data = json.load(json_data)
        data = json.dumps(data)
        response = self.client.post(
            self.URL,
            data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400, "Add duplicated access info")
        self.client.logout()


class AccessInfoGroupDetail(APITestCase):
    URL = "/api/v1/access/group/1/1"

    @classmethod
    def setUpTestData(self):
        print("")
        print("Access Group Detail Info GET / PUT / DELETE")
        self.group = Group.objects.create(name="TestGroup")
        self.other_group = Group.objects.create(name="TestGroup2")
        self.test_user = User.objects.create(
            username="testuser",
            email="art970@naver.com",
        )
        self.test_user_group_coach = User.objects.create(
            username="testCoach",
            email="kdh97048@gmail.com",
            is_coach=True,
            group=self.group,
        )
        self.test_user_other_coach = User.objects.create(
            username="testOtherCoach",
            email="kdh97049@gmail.com",
            is_coach=True,
            group=self.other_group,
        )
        with open(
            "./post_test/access/new_post_example.json", "r", encoding="UTF-8"
        ) as json_data:
            data = json.load(json_data)
        for i in data.get("members"):
            AccessInfo.objects.create(
                name=i.get("name"),
                email=i.get("email"),
                phone_number=i.get("phone_number"),
                group=self.group,
            )
        self.other_access_info = AccessInfo.objects.create(
            name="test",
            email="test@test.com",
            phone_number="01088848077",
            group=self.other_group,
        )

    def test_view_access_info_group_detail_non_login_user(self):
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, 403, "Non login user")

    def test_view_access_info_group_detail_login_normal_user(self):
        self.client.force_login(self.test_user)
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, 403, "login normal user")
        self.client.logout()

    def test_view_access_info_group_detail_login_coach_user(self):
        self.client.force_login(self.test_user_group_coach)
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, 200, "login coach user")
        self.client.logout()

    def test_view_access_info_group_detail_login_other_coach_user(self):
        self.client.force_login(self.test_user_other_coach)
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, 403, "login other coach user")
        self.client.logout()

    def test_view_access_info_group_detail_other_group_pk_access(self):
        self.client.force_login(self.test_user_group_coach)
        response = self.client.get(
            f"/api/v1/access/group/1/{self.other_access_info.pk}"
        )
        self.assertEqual(
            response.status_code,
            404,
            "login group access info pk access",
        )
        self.client.logout()

    def test_edit_access_info_group_detail_non_login_user(self):
        response = self.client.put(self.URL)
        self.assertEqual(response.status_code, 403, "Non login user")

    def test_edit_access_info_group_detail_login_normal_user(self):
        self.client.force_login(self.test_user)
        response = self.client.put(self.URL)
        self.assertEqual(response.status_code, 403, "Non login user")
        self.client.logout()
