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

