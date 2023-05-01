from rest_framework.test import APITestCase
from .models import Category
from groups.models import Group
from . import serializers
from users.models import User


# 카테고리 조회 테스트
class CategoriesGet(APITestCase):
    URL = "/api/v1/categories/"
    NAME = "Category Test"

    def setUp(self):
        self.GROUP = Group.objects.create(name="oz")
        Category.objects.create(
            name=self.NAME,
            group=self.GROUP,
        )

    def test_all_category(self):
        response = self.client.get(self.URL)
        data = response.json()
        self.assertEqual(response.status_code, 200, "status isn't 200")
        self.assertEqual(len(response.data), 4)


# 그룹 카테고리 조회 테스트


# 그룹 카테고리 생성 테스트
class CategoriesPost(APITestCase):
    URL = "/api/v1/categories/"
    NAME = "Category Test"

    def setUp(self):
        self.GROUP = Group.objects.create(name="oz")
        self.user = User.objects.create(is_coach=True)
        self.category = Category.objects.create(
            name=self.NAME,
            group=self.GROUP,
        )

    def test_category_post_with_valid_data(self):
        # 유효한 데이터로 POST 요청 보내기
        data = {"name": "study"}
        self.client.force_login(self.user)
        response = self.client.post(f"{self.URL}{self.GROUP.pk}", data, format="json")
        # 응답 코드가 201인지 확인
        self.assertEqual(response.status_code, 201)

        # 응답 데이터가 올바른지 확인
        # category = self.GROUP.categories.first()
        # serializer = serializers.CategorySerializer(category)
        # self.assertEqual(response.data, data)

    def test_category_post_with_invalid_data(self):
        # 유효하지 않은 데이터로 POST 요청 보내기
        data = {"name": ""}
        self.client.force_login(self.user)
        response = self.client.post(f"{self.URL}{self.GROUP.pk}", data, format="json")
        # 응답 코드가 400인지 확인
        self.assertEqual(response.status_code, 400)

        # 에러 메시지가 올바른지 확인
        # expected_error = {"name": ["This field may not be blank."]}
        # self.assertEqual(response.data, expected_error)

    def test_category_post_without_permission(self):
        # 권한이 없는 사용자로 POST 요청 보내기
        self.client.login(username="testuser", password="testpass")
        data = {"name": "Category A"}
        # response = self.client.post(self.URL, data, content_type="application/json")

        # 응답 코드가 403인지 확인
        response = self.client.get(f"{self.URL}{self.GROUP.pk}")
        self.assertEqual(response.status_code, 403)


# 그룹 카테고리 수정 테스트
class CategoriesPut(APITestCase):
    URL = "/api/v1/categories/"
    NAME = "Change test"

    def setUp(self):
        self.GROUP = Group.objects.create(name="oz")
        self.upload_user = User.objects.create(username="Test User")
        self.category = Category.objects.create(
            name=self.NAME,
            group=self.GROUP,
        )

    # 존재하지 않는 url 접근
    def test_view_category_detail_not_found_url(self):
        self.client.force_login(self.upload_user)
        response = self.client.get(f"{self.URL}/10", format="json")
        self.assertEqual(response.status_code, 404, "존재하지 않는 url")
        self.client.logout()

    # 비 로그인 유저가 수정
    def test_edit_category_detail_non_login_user(self):
        data = {"name": "study"}
        response = self.client.put(
            f"{self.URL}{self.GROUP.pk}{self.category.pk}", data, format="json"
        )
        self.assertEqual(response.status_code, 403, "비 로그인 수정")

    # 생성한 유저가 아닌 유저가 수정
    def test_edit_category_detail_not_create_user(self):
        user = User.objects.create(name="OtherUser", email="user@example.com")
        self.client.force_login(user)
        response = self.client.put(
            f"{self.URL}{self.GROUP.pk}/{self.category.pk}/",
            data={"name": "Change test"},
            format="json",
        )
        self.assertEqual(response.status_code, 403, "로그인 (업로드 유저가 아닌 유저) 후 수정")
        self.client.logout()

    # 생성한 유저가 수정
    # def test_edit_category_detail_create_user(self):
    #     self.client.force_login(self.upload_user)
    #     response = self.client.put(
    #         f"{self.URL}{self.GROUP.pk}/{self.category.pk}/",
    #         data={"name": "Change test"},
    #         format="json",
    #     )
    #     self.assertEqual(response.status_code, 200, "로그인 (업로드 유저) 후 수정")
    #     self.client.logout()

    # 수정 확인
    def test_edit_task_detail_create_user_change_value(self):
        self.client.force_login(self.upload_user)
        response = self.client.put(
            f"{self.URL}{self.GROUP.pk}/{self.category.pk}/",
            data={"name": "Change test"},
            format="json",
        )
        self.assertEqual(
            Category.objects.get(pk=self.category.pk).name,
            "Change test",
            "수정 여부 확인",
        )
        self.client.logout()
