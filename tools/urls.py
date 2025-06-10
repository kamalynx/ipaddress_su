from django.urls import path
from django.views.generic import TemplateView

from . import views


app_name = "tools"

urlpatterns = [
    path(
        "", TemplateView.as_view(template_name="tools/tools.html"), name="main"
    ),
    path("nslookup/", views.nslookup_view, name="nslookup"),
    path("nslookup/<domain>/", views.nslookup_view, name="nslookup_with_domain"),
    path("ipinfo/", views.ipinfo_view, name="ipinfo"),
    path("ipinfo/<ip>/", views.ipinfo_with_ip, name="ipinfo_with_ip"),
    path("ipcalc/", views.ipcalc_view, name="ipcalc"),
]
