from pytest_django.asserts import assertTemplateUsed

from tools import views


def test_ipcalc_template_used(client):
    response = client.get('/tools/ipcalc/')
    assertTemplateUsed(response, 'tools/ipcalc.html')
    assert response.resolver_match.func == views.ipcalc_view
