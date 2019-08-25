from django.http import JsonResponse
from django.test import TestCase, RequestFactory
from django.views.generic import ListView

from forum.forms import TestAjaxForm
from forum.views import MultiAjaxHandler


class TestMultiAjaxHandler(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.majax = MultiAjaxHandler()
        self.majax.handler_dict = {
            'action1': 'form1',
            'action2': 'form2',
        }

    def test_request_is_valid_noajax(self):
        data = {
            'action': 'action1',
        }
        request = self.factory.post('test/path', data=data)
        self.majax.request = request
        self.assertFalse(self.majax.request_is_valid())

    def test_request_is_valid_wrong_action(self):
        data = {
            'action': 'doesnotexist',
        }
        request = self.factory.post('test/path', data=data)
        self.majax.request = request
        self.assertFalse(self.majax.request_is_valid())

    def test_request_is_valid_no_data(self):
        data = {}
        request = self.factory.post('test/path', data=data)
        self.majax.request = request
        self.assertFalse(self.majax.request_is_valid())

    def test_request_is_valid_withajax(self):
        data = {
            'action': 'action1',
        }
        request = self.factory.post('test/path', data=data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.majax.request = request
        self.assertTrue(self.majax.request_is_valid())

    def test_request_is_valid_withajax_wrongdata(self):
        data = {
            'action': 'wrongaction',
        }
        request = self.factory.post('test/path', data=data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.majax.request = request
        self.assertFalse(self.majax.request_is_valid())

    # Test that the correct dict value is returned
    def test_ajax_router(self):
        data = {
            'action': 'action2',
        }
        request = self.factory.post('test/path', data=data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.majax.request = request
        self.assertEqual(self.majax.action_router(), 'form2')
