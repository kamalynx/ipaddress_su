import pytest
from django.core.exceptions import ValidationError
from netaddr import valid_ipv4

from tools import forms


def test_valid_ipv4_form():
    form_data = {"ipaddress": "192.168.1.1", "netmask": "24"}
    form = forms.IPv4CalcForm(data=form_data)
    assert form.is_valid()
    assert valid_ipv4(form.cleaned_data["ipaddress"])


def test_invalid_ipv4_form():
    form_data = {"ipaddress": "256.0.256.0", "netmask": "24"}
    form = forms.IPv4CalcForm(data=form_data)
    assert not form.is_valid()
    assert "ipaddress" in form.errors


def test_all_masks_valid():
    for cidr, _ in forms.subnet_masks:
        form = forms.IPv4CalcForm(
            data={"ipaddress": "192.168.1.1", "netmask": cidr}
        )
        assert form.is_valid(), f"Failed for CIDR: {cidr}"
