from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

from WGForge.cats.models import Cats

from .factories import CatsFactory


class CatCreateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        CatsFactory.create_batch(15)
        self.cats = Cats.objects.all().values()

    def test_base_functional(self):
        payload = """{\"name\": \"Tihon\", \"color\": \"red & white\", \"tail_length\": 15, \"whiskers_length\": 12}"""  # noqa E501
        response = self.client.post(
            reverse("cat_create"),
            data=payload,
            content_type="application/x-www-form-urlencoded",
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(
            "Data successfully added", response.content.decode("utf-8")
        )
        response = self.client.post(
            reverse("cat_create"),
            data=payload,
            content_type="application/x-www-form-urlencoded",
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertIn(
            "Cats with this Name already exists",
            response.content.decode("utf-8"),
        )

    def test_bad_requests(self):
        payload = """{\"name\": \"Tihon\", \"color\": \"red & white\", \"tail_length\": -15, \"whiskers_length\": 12}"""  # noqa E501
        response = self.client.post(
            reverse("cat_create"),
            data=payload,
            content_type="application/x-www-form-urlencoded",
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertIn(
            "tail_length",
            response.content.decode("utf-8"),
        )

        payload = """{\"name\": \"Tihon\", \"color\": \"red & white\", \"tail_length\": \"Tihon\", \"whiskers_length\": 12}"""  # noqa E501
        response = self.client.post(
            reverse("cat_create"),
            data=payload,
            content_type="application/x-www-form-urlencoded",
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertIn(
            "tail_length",
            response.content.decode("utf-8"),
        )

        payload = """{\"name\": \"Tihon\", \"color\": \"red & white\","""
        response = self.client.post(
            reverse("cat_create"),
            data=payload,
            content_type="application/x-www-form-urlencoded",
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertIn(
            "This field is required.",
            response.content.decode("utf-8"),
        )

        payload = """{\"name\": \"Tihon\", \"color\": \"red & white\", \"tail_length\": 1000000, \"whiskers_length\": 12}"""  # noqa E501
        response = self.client.post(
            reverse("cat_create"),
            data=payload,
            content_type="application/x-www-form-urlencoded",
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertIn(
            "tail_length",
            response.content.decode("utf-8"),
        )
