from django.test import TestCase, RequestFactory
from ipware import get_client_ip

from .views import HomePage


class HomePageTest(TestCase):

    def test_ip_address_in_context(self):
        """Test, if client ip in context data, and its equals."""

        request = RequestFactory().get('/')
        view = HomePage()
        view.setup(request)
        context = view.get_context_data()

        client_ip = get_client_ip(view.request)[0]

        self.assertIn('ipaddress', context)
        self.assertEqual(client_ip, context.get('ipaddress'))
