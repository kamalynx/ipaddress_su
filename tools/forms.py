from django import forms
from django.core.validators import DomainNameValidator, validate_ipv46_address


class DomainForm(forms.Form):
    domain = forms.CharField(
        label="домен",
        widget=forms.TextInput(attrs={"class": "form__field"}),
        validators=[DomainNameValidator()],
    )


class IPForm(forms.Form):
    ipaddress = forms.GenericIPAddressField(
        label="IP адрес",
        widget=forms.TextInput(attrs={"class": "form__field"}),
        unpack_ipv4=True,
        validators=[validate_ipv46_address],
    )
