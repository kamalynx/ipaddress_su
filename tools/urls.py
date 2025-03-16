from django.urls import path

from . import views


app_name = "tools"

urlpatterns = [
    path("", views.tools_home, name="main"),
    path("nslookup/", views.nslookup, name="nslookup"),
    path("nslookup/<domain>/", views.nslookup, name="nslookup_with_domain"),
    path("ipinfo/", views.whois, name="whois"),
    path("ipinfo/<input_ipaddress>/", views.whois, name="whois_with_ip"),
    #path("whois/", views.whois_domain, name="whois_domain"),
    #path("whois/<domain_name>/", views.whois_domain, name="whois_with_domain"),
]
