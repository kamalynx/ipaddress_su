from django import forms
from django.core.validators import DomainNameValidator, validate_ipv46_address


subnet_masks = [
    (0, "0.0.0.0 - /0"),
    (1, "128.0.0.0 - /1"),
    (2, "192.0.0.0 - /2"),
    (3, "224.0.0.0 - /3"),
    (4, "240.0.0.0 - /4"),
    (5, "248.0.0.0 - /5"),
    (6, "252.0.0.0 - /6"),
    (7, "254.0.0.0 - /7"),
    (8, "255.0.0.0 - /8"),
    (9, "255.128.0.0 - /9"),
    (10, "255.192.0.0 - /10"),
    (11, "255.224.0.0 - /11"),
    (12, "255.240.0.0 - /12"),
    (13, "255.248.0.0 - /13"),
    (14, "255.252.0.0 - /14"),
    (15, "255.254.0.0 - /15"),
    (16, "255.255.0.0 - /16"),
    (17, "255.255.128.0 - /17"),
    (18, "255.255.192.0 - /18"),
    (19, "255.255.224.0 - /19"),
    (20, "255.255.240.0 - /20"),
    (21, "255.255.248.0 - /21"),
    (22, "255.255.252.0 - /22"),
    (23, "255.255.254.0 - /23"),
    (24, "255.255.255.0 - /24"),
    (25, "255.255.255.128 - /25"),
    (26, "255.255.255.192 - /26"),
    (27, "255.255.255.224 - /27"),
    (28, "255.255.255.240 - /28"),
    (29, "255.255.255.248 - /29"),
    (30, "255.255.255.252 - /30"),
    (31, "255.255.255.254 - /31"),
    (32, "255.255.255.255 - /32"),
]


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


class IPv4CalcForm(forms.Form):
    ipaddress = forms.GenericIPAddressField(
        label="IP адрес",
        widget=forms.TextInput(attrs={"class": "form__field"}),
        protocol="IPv4",
    )
    netmask = forms.ChoiceField(
        label="Маска подсети",
        widget=forms.Select(attrs={"class": "form__field"}),
        choices=subnet_masks,
        initial=24,
    )
