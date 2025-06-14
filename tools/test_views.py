import pytest
import validators
from django.urls import reverse_lazy
from pytest_django.asserts import assertTemplateUsed, assertRedirects

from tools import views


def test_ipcalc_template_used(client):
    response = client.get('/tools/ipcalc/')
    assertTemplateUsed(response, 'tools/ipcalc.html')
    assert response.resolver_match.func == views.ipcalc_view


@pytest.mark.django_db
def test_whois_view_func(client):
    response = client.get(reverse_lazy('tools:whois'))
    assertTemplateUsed(response, 'tools/whois.html')
    assert 'log' in response.context
    assert 'form' in response.context
    assert response.resolver_match.func == views.whois_view


@pytest.mark.django_db
def test_whois_with_ip_view_func(client):
    response = client.get(
        reverse_lazy('tools:whois_with_domain', kwargs={'domain': 'example.com'})
    )
    assert response.resolver_match.func == views.whois_with_domain

    for variable in ('form', 'domain', 'log', 'result'):
        assert variable in response.context

    assert validators.domain(response.context['domain'])


@pytest.mark.django_db
def test_whois_with_ip_invalid_domain(client):
    response = client.get(
        reverse_lazy('tools:whois_with_domain', kwargs={'domain': 'localhost'})
    )
    assert not validators.domain(response.context['domain'])
