import json

from django.test import Client, TestCase
from WGForge.cats.models import Cats

from .factories import CatsFactory

BASE_URL = "http://localhost:8080/"


def is_equal_str_item_and_queryset(item, qs):
    item_list = json.loads(item)
    qs_list = list(qs)
    return [el for el in item_list if el not in qs_list] == []


class CatListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        CatsFactory.create_batch(15)
        self.cats = Cats.objects.all().values()

    def test_list_cats(self):
        response = self.client.get(BASE_URL + "cats")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            is_equal_str_item_and_queryset(response.content, self.cats)
        )

    def test_list_cats_attribute_sort_limit_offset(self):
        response = self.client.get(BASE_URL + "cats?attribute=name&order=asc")
        self.assertEqual(response.status_code, 200)
        qs = self.cats.values("name").order_by("name")
        self.assertTrue(is_equal_str_item_and_queryset(response.content, qs))

        response = self.client.get(
            BASE_URL + "cats?attribute=tail_length&order=desc"
        )
        self.assertEqual(response.status_code, 200)
        qs = self.cats.values("tail_length").order_by("-tail_length")
        self.assertTrue(is_equal_str_item_and_queryset(response.content, qs))

        response = self.client.get(BASE_URL + "cats?offset=10&limit=10")
        self.assertEqual(response.status_code, 200)
        qs = self.cats[10:20]
        self.assertTrue(is_equal_str_item_and_queryset(response.content, qs))

        response = self.client.get(
            BASE_URL + "cats?attribute=color&order=asc&offset=5&limit=2"
        )
        self.assertEqual(response.status_code, 200)
        qs = self.cats.values("color").order_by("color")[5:7]
        self.assertTrue(is_equal_str_item_and_queryset(response.content, qs))

    def test_list_cats_bad_request(self):
        response = self.client.get(BASE_URL + "cats?attribute=AAA")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.content.decode("utf-8"), "HTTP 400 Bad Request"
        )

        response = self.client.get(BASE_URL + "cats?order=AAA")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.content.decode("utf-8"), "HTTP 400 Bad Request"
        )

        response = self.client.get(BASE_URL + "cats?order=asc")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.content.decode("utf-8"), "HTTP 400 Bad Request"
        )

        response = self.client.get(BASE_URL + "cats?offset=500")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_equal_str_item_and_queryset(response.content, []))
