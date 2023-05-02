from rest_framework.test import APITestCase
from .models import Feed
from groups.models import Group
from users.models import User
from categories.models import Category


# 게시글 디테일 조회.수정.삭제 테스트
# 댓글 생성 테스트
# 대댓글 생성 테스트
# 게시글 검색
# 게시글 검색 결과
# 그룹 카테고리 게시글 조회


# 게시글 조회 테스트
class FeedGet(APITestCase):
    URL = "/api/v1/feeds/"
    TITLE = "feed get test"

    def setUp(self):
        self.user = User.objects.create(is_coach=True)
        self.feed = Feed.objects.create(
            title=self.TITLE,
        )

    def get_all_feed(self):
        self.client.force_login(self.user)
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, 200, "status isn't 200")
        self.assertEqual(len(response.data), 4)


# 게시글 생성 테스트
class FeedGet(APITestCase):
    URL = "/api/v1/feeds/"
    TITLE = "feed get test"

    def setUp(self):
        self.group = Group.objects.create(name="oz")
        self.user = User.objects.create(is_coach=True, group=self.group)
        self.category = Category.objects.create(group=self.group)
        self.feed = Feed.objects.create(
            user=self.user,
            title=self.TITLE,
            category=self.category,
        )

    def get_all_feed(self):
        self.client.force_login(self.user)
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, 200, "status isn't 200")
        self.assertEqual(len(response.data), 4)

    # 유효한 데이터로 POST 요청 보내기
    def test_feed_post_with_valid_data(self):
        data = {"title": "first feed", "category": 1}
        self.client.force_login(self.user)
        response = self.client.post(self.URL, data, format="json")
        print(response.data)
        self.assertEqual(response.status_code, 200)

    # # 유효하지 않은 데이터로 POST 요청 보내기
    # def test_category_post_with_invalid_data(self):
    #     data = {"name": ""}
    #     self.client.force_login(self.user)
    #     response = self.client.post(f"{self.URL}{self.group.pk}", data, format="json")
    #     self.assertEqual(response.status_code, 400)

    # # 권한이 없는 사용자로 POST 요청 보내기
    # def test_category_post_without_permission(self):
    #     self.client.login(username="testuser", password="testpass")
    #     data = {"name": "Category A"}
    #     response = self.client.get(f"{self.URL}{self.group.pk}")
    #     self.assertEqual(response.status_code, 403)


# # 그룹 카테고리 수정 테스트
# class GroupCategoriesPut(APITestCase):
#     URL = "/api/v1/categories/"
#     NAME = "Change test"

#     def setUp(self):
#         self.group = Group.objects.create(name="oz")
#         self.upload_user = User.objects.create(
#             username="Test User",
#             is_coach=True,
#             group=self.group,
#         )
#         self.category = Category.objects.create(
#             name=self.NAME,
#             group=self.group,
#         )

#     # 존재하지 않는 url 접근
#     def test_view_category_detail_not_found_url(self):
#         self.client.force_login(self.upload_user)
#         response = self.client.get(f"{self.URL}/10", format="json")
#         self.assertEqual(response.status_code, 404, "존재하지 않는 url")
#         self.client.logout()

#     # 비 로그인 유저가 수정
#     def test_edit_category_detail_non_login_user(self):
#         response = self.client.put(
#             f"{self.URL}{self.group.pk}/{self.category.pk}/",
#             data={"name": "Change test"},
#             format="json",
#         )
#         self.assertEqual(response.status_code, 403, "비 로그인 수정")

#     # 생성한 유저가 아닌 유저가 수정
#     def test_edit_category_detail_not_create_user(self):
#         user = User.objects.create(
#             name="OtherUser", email="user@example.com", is_coach=True
#         )
#         self.client.force_login(user)
#         response = self.client.put(
#             f"{self.URL}{self.group.pk}/{self.category.pk}/",
#             data={"name": "Change test"},
#             format="json",
#         )
#         self.assertEqual(response.status_code, 403, "로그인 (업로드 유저가 아닌 유저) 후 수정")
#         self.client.logout()

#     # 생성한 유저가 수정
#     def test_edit_category_detail_create_user(self):
#         self.client.force_login(self.upload_user)
#         response = self.client.put(
#             f"{self.URL}{self.group.pk}/{self.category.pk}/",
#             data={"name": "Change test"},
#             format="json",
#         )
#         self.assertEqual(response.status_code, 200, "로그인 (업로드 유저) 후 수정")
#         self.client.logout()

#     # 수정 확인
#     def test_edit_task_detail_create_user_change_value(self):
#         self.client.force_login(self.upload_user)
#         response = self.client.put(
#             f"{self.URL}{self.group.pk}/{self.category.pk}/",
#             data={"name": "Change test"},
#             format="json",
#         )
#         self.assertEqual(
#             Category.objects.get(pk=self.category.pk).name,
#             "Change test",
#             "수정 여부 확인",
#         )
#         self.client.logout()
