from rest_framework.test import APITestCase
from .models import Category
from groups.models import Group


# path("api/v1/categories/", include("categories.urls")),
class CategoriesTests(APITestCase):
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
        self.assertEqual(
            response.status_code,
            200,
            "status isn't 200",
        )


# path("<int:group_pk>", views.GroupCategories.as_view()),


# ----------------------------------------------------------------
#     def setUp(self):
#         self.url = reverse("categories")
#         self.category1 = Category.objects.create(name="Category 1")
#         self.category2 = Category.objects.create(name="Category 2")

#     def test_get_all_categories(self):
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 2)

#     def test_get_non_existing_category(self):
#         url = reverse("group_categories", kwargs={"group_pk": 1})
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     def test_create_category_unauthenticated(self):
#         data = {"name": "New Category"}
#         response = self.client.post(self.url, data)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_create_category_without_permission(self):
#         user = get_user_model().objects.create_user(
#             username="testuser",
#             password="testpass",
#         )
#         token = Token.objects.create(user=user)
#         self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
#         data = {"name": "New Category"}
#         response = self.client.post(self.url, data)
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#     def test_create_category(self):
#         group = Group.objects.create(name="Test Group")
#         user = get_user_model().objects.create_user(
#             username="testuser",
#             password="testpass",
#             group=group,
#             is_coach=True,
#         )
#         token = Token.objects.create(user=user)
#         self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
#         data = {"name": "New Category", "group": group.id}
#         response = self.client.post(self.url, data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Category.objects.count(), 3)


# class GroupCategoriesTests(APITestCase):
#     def setUp(self):
#         self.group = Group.objects.create(name="Test Group")
#         self.url = reverse("group_categories", kwargs={"group_pk": self.group.id})
#         self.category1 = Category.objects.create(name="Category 1", group=self.group)
#         self.category2 = Category.objects.create(name="Category 2", group=self.group)

#     def test_get_group_categories(self):
#         user = get_user_model().objects.create_user(
#             username="testuser",
#             password="testpass",
#             group=self.group,
#         )
#         token = Token.objects.create(user=user)
#         self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 2)

#     def test_create_category_without_permission(self):
#         user = get_user_model().objects.create_user(
#             username="testuser",
#             password="testpass",
#         )
#         token = Token.objects.create(user=user)
#         self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
#         data = {"name": "New Category", "group": self.group.id}
#         response = self.client.post(self.url, data)
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#     def test_create_category(self):
#         user = get_user_model
