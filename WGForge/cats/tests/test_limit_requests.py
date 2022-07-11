import time
from http import HTTPStatus

from django.test import Client, TestCase, override_settings
from django.urls import reverse

from .factories import CatsFactory

TEST_LIMIT_TIME = 10
TESTING_THRESHOLD = 5
CAT_VIEW_TESTING_LIMIT = {
    "PATH": reverse("cats_view"),
    "METHOD": "GET",
    "LIMIT": "5/m",
    "CACHE_NAME": "cat_view_limit",
}


class SlowTestException(Exception):
    pass


class CatsTestCaseMixin:
    def _callTestMethod(self, method):
        start = time.time()
        result = super()._callTestMethod(method)
        limit_seconds = TEST_LIMIT_TIME
        time_taken = time.time() - start
        if time_taken > limit_seconds:
            raise SlowTestException(
                f"This test took {time_taken:.2f}s, "
                + f"more than the limit of {limit_seconds}s."
            )
        return result


class CatListViewLimitTest(CatsTestCaseMixin, TestCase):
    def setUp(self):
        self.client = Client()
        CatsFactory.create_batch(15)

    @override_settings(CAT_VIEW_LIMIT=CAT_VIEW_TESTING_LIMIT)
    def test_rate_limit(self):
        url = reverse("cats_view")
        for i in range(0, TESTING_THRESHOLD):
            self.client.get(url)
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.TOO_MANY_REQUESTS)
