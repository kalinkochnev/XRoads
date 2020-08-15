from XroadsAPI.mixins import *
import pytest
from rest_framework.test import APIRequestFactory


class TestAddAdminMixin:
    def valid_post_request(self):
        factory = APIRequestFactory()
        body = {
            ''
        }
        factory.post('some-url/', )

class TestRemoveAdminMixin:
    def valid_post_request(self):
        pass