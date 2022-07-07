import json
import urllib.parse as urlparse
from http import HTTPStatus
from urllib.parse import urlencode

from django.test import Client, TestCase
from django.urls import reverse

from WGForge.cats.models import Cats

from .factories import CatsFactory


def is_equal_str_item_and_queryset(item, qs):
    item_list = json.loads(item)
    qs_list = list(qs)
    return [el for el in item_list if el not in qs_list] == []


class CatListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        CatsFactory.create_batch(15)
        self.cats = Cats.objects.all().values()
        self.base_url = reverse("cats_view")

    def _create_url_with_parameters(self, url, params):
        # https://stackoverflow.com/questions/2506379/add-params-to-given-url-in-python
        url_parts = list(urlparse.urlparse(url))
        query = dict(urlparse.parse_qsl(url_parts[4]))
        query.update(params)
        url_parts[4] = urlencode(query)
        return urlparse.urlunparse(url_parts)

    def test_list_cats(self):
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(
            is_equal_str_item_and_queryset(response.content, self.cats)
        )

    def test_list_cats_attribute_sort_limit_offset(self):

        params = {"attribute": "name", "order": "asc"}
        url = self._create_url_with_parameters(self.base_url, params)

        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        qs = self.cats.values("name").order_by("name")
        self.assertTrue(is_equal_str_item_and_queryset(response.content, qs))

        params = {"attribute": "tail_length", "order": "desc"}
        url = self._create_url_with_parameters(self.base_url, params)

        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        qs = self.cats.values("tail_length").order_by("-tail_length")
        self.assertTrue(is_equal_str_item_and_queryset(response.content, qs))

        params = {"offset": "10", "limit": "10"}
        url = self._create_url_with_parameters(self.base_url, params)

        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        qs = self.cats[10:20]
        self.assertTrue(is_equal_str_item_and_queryset(response.content, qs))

        params = {
            "attribute": "color",
            "order": "asc",
            "offset": "5",
            "limit": "2",
        }
        url = self._create_url_with_parameters(self.base_url, params)

        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        qs = self.cats.values("color").order_by("color")[5:7]
        self.assertTrue(is_equal_str_item_and_queryset(response.content, qs))

    def test_list_cats_bad_request(self):

        params = {"attribute": "AAA"}
        url = self._create_url_with_parameters(self.base_url, params)

        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(
            response.content.decode("utf-8"), "HTTP 400 Bad Request"
        )

        params = {"order": "AAA"}
        url = self._create_url_with_parameters(self.base_url, params)

        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(
            response.content.decode("utf-8"), "HTTP 400 Bad Request"
        )

        params = {"order": "asc"}
        url = self._create_url_with_parameters(self.base_url, params)

        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(
            response.content.decode("utf-8"), "HTTP 400 Bad Request"
        )

        params = {"offset": "500"}
        url = self._create_url_with_parameters(self.base_url, params)

        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(is_equal_str_item_and_queryset(response.content, []))
