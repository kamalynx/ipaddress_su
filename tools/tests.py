from datetime import datetime

import pytest
from netaddr import valid_ipv4, valid_ipv6
from django.test import TestCase, RequestFactory
from ipware import get_client_ip

from .views import HomePage
from . import forms, models


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

    def test_template(self):
        request = self.client.get('/')
        self.assertTemplateUsed(request, 'main.html')


class TestDomainForm(TestCase):
    def test_form_valid(self):
        form = forms.DomainForm(data={'domain': 'example.com'})
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        self.assertFalse(forms.DomainForm({'domain': 'localhost'}).is_valid())
        self.assertFalse(forms.DomainForm({'domain': '123'}).is_valid())
        self.assertFalse(
            forms.DomainForm({'domain': 'https://example.com'}).is_valid()
        )
        self.assertFalse(
            forms.DomainForm({'domain': 'http://localhost'}).is_valid()
        )
        self.assertFalse(forms.DomainForm({'domain': '127.0.0.1'}).is_valid())


class TestIPForm(TestCase):
    def test_form_valid(self):
        form = forms.IPForm({'ipaddress': '10.0.0.1'})
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        self.assertFalse(forms.IPForm({'ipaddress': '127.0.0.256'}).is_valid())
        self.assertFalse(
            forms.IPForm({'ipaddress': 'just a string'}).is_valid()
        )


@pytest.fixture
def iplog_model():
    return models.IPLog.objects.create(address='127.0.0.1')


@pytest.mark.django_db
def test_sample_model_ip(iplog_model):
    assert iplog_model.address == '127.0.0.1'
    assert isinstance(iplog_model.address, str)
    assert valid_ipv4(iplog_model.address)
