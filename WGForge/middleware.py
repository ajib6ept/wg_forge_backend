import hashlib

from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse

SECONDS_LIMITS = {"s": 1, "m": 60, "h": 60 * 60, "d": 60 * 60 * 24}


class CatLimitViewMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.cat_limit_view_cashe = 0

    def __call__(self, request):

        response = self.get_response(request)

        self.cache_limit_settings = getattr(settings, "CAT_VIEW_LIMIT", False)
        if not self.cache_limit_settings:
            return response

        limit_request_settings = self.cache_limit_settings["LIMIT"].split("/")
        limit_request_value = int(limit_request_settings[0])
        limit_request_period = SECONDS_LIMITS.get(limit_request_settings[1])

        if self.is_this_request_limited(request):
            key = self.make_key(request)
            if self.is_request_limit_exceeded(key, limit_request_value):
                return JsonResponse({"error": "ratelimited"}, status=429)
            else:
                self.save_key(key, limit_request_period)
        return response

    def make_key(self, request):
        key_string = (request.method + request.path).encode("utf-8")
        return hashlib.md5(key_string).hexdigest()

    def save_key(self, key, limit_time):
        added = cache.add(key, 1, limit_time)
        if not added:
            cache.incr(key)

    def is_request_limit_exceeded(self, key, limit):
        value = cache.get(key, 0)
        if value + 1 > limit:
            return True
        return False

    def is_this_request_limited(self, request):
        if (
            str(request.method) == self.cache_limit_settings["METHOD"]
            and str(request.path) == self.cache_limit_settings["PATH"]
        ):
            return True
        return False

    def process_exception(self, request, exception):
        return None
