from collections.abc import Iterable

import pytest
from netaddr import valid_ipv4, valid_ipv6

from tools import helpers


class TestIpInfo:
    def test_success_get_ip_info(self):
        ipinfo = helpers.get_ip_info('212.33.245.31')
        assert ipinfo.status == 'success'
        assert ipinfo.query == '212.33.245.31'
        assert isinstance(ipinfo, helpers.IPInfo)

    def test_reserved_get_ip_info(self):
        ipinfo = helpers.get_ip_info('127.0.0.1')
        assert ipinfo.status == 'fail'
        assert ipinfo.message == 'reserved range'
        assert isinstance(ipinfo, helpers.IPError)

    def test_invlid_ip_get_info(self):
        ipinfo = helpers.get_ip_info('some of shit')
        assert ipinfo.status == 'fail'
        assert ipinfo.message == 'invalid query'
        assert isinstance(ipinfo, helpers.IPError)


def test_nslookup():
    ips = helpers.nslookup('ya.ru')
    for ip4 in ips[0]:
        assert valid_ipv4(ip4)

    for ip6 in ips[1]:
        assert valid_ipv6(ip6)
