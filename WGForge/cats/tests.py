from django.test import Client, TestCase


class CatsBaseTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_ping(self):
        response = self.client.get("http://localhost:8080/ping")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content.decode("utf-8"), "Cats Service. Version 0.1"
        )
