from rest_framework.test import APITestCase
from .models import Category
from groups.models import Group
from . import serializers


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
        # data = response.json()
        self.assertEqual(response.status_code, 200, "status isn't 200")
        self.assertEqual(len(response.data), 3)


# 그룹 카테고리 조회 테스트


# 그룹 카테고리 생성 테스트
class CategoryPost(APITestCase):
    URL = "/api/v1/categories/"
    NAME = "Category Test"

    def setUp(self):
        self.GROUP = Group.objects.create(name="oz")
        self.category = Category.objects.create(
            name=self.NAME,
            group=self.GROUP,
        )

    def test_category_post_with_valid_data(self):
        # 유효한 데이터로 POST 요청 보내기
        data = {"name": "oz"}
        # response = self.client.post(self.URL, data, content_type="application/json")

        # 응답 코드가 201인지 확인
        # self.assertEqual(response.status_code, 201)

        # 응답 데이터가 올바른지 확인
        # category = self.GROUP.categories.first()
        # serializer = serializers.CategorySerializer(category)
        # self.assertEqual(response.data, data)

    def test_category_post_with_invalid_data(self):
        # 유효하지 않은 데이터로 POST 요청 보내기
        data = {"name": ""}
        response = self.client.post(self.URL, data, content_type="application/json")

        # 응답 코드가 400인지 확인
        # self.assertEqual(response.status_code, 400)

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
