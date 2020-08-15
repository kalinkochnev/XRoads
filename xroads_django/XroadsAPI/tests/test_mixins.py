from XroadsAPI.mixins import *

class DummyAddAdmin(AddAdminMixin):
    pass

class TestAddAdminMixin:
    def valid_post_request(self):
        pass

class TestRemoveAdminMixin:
    def valid_post_request(self):
        pass