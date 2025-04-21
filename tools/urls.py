from django.urls import path
from django.views.generic import TemplateView

from . import views


app_name = "tools"

urlpatterns = [
    path("", TemplateView.as_view(template_name='tools/tools.html'), name="main"),
    path("nslookup/", views.nslookup, name="nslookup"),
    path("nslookup/<domain>/", views.nslookup, name="nslookup_with_domain"),
    # ~ path("ipinfo/", views.whois, name="whois"),
    # ~ path("ipinfo/<input_ipaddress>/", views.whois, name="whois_with_ip"),
    path("whois/", views.WhoisView.as_view(), name="whois"),
    path("whois/<domain_name>/", views.WhoisView.as_view(), name="whois_with_domain"),
]
