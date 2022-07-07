from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse


class CatsBaseTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_ping(self):
        response = self.client.get(reverse("ping_service"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(
            response.content.decode("utf-8"), "Cats Service. Version 0.1"
        )
