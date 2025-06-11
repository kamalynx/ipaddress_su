import logging
from io import BytesIO
from time import monotonic

import dns.resolver
import httpx
from dns.exception import DNSException
from attrs import define


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@define
class IPInfo:
    status: str
    country: str
    countryCode: str
    regionName: str
    city: str
    lat: float
    lon: float
    timezone: str
    isp: str
    org: str
    reverse: str
    mobile: bool
    proxy: bool
    query: str
    asn: str


@define
class IPError:
    status: str
    message: str
    query: str


def nslookup(domain):
    ipsv4, ipsv6 = None, None

    try:
        ipsv4 = dns.resolver.resolve(domain, 'a')
    except DNSException as err:
        ipsv4 = err

    try:
        ipsv6 = dns.resolver.resolve(domain, 'aaaa')
    except DNSException as err:
        ipsv6 = err

    return ipsv4, ipsv6


async def get_dns_records(domain):
    common_records = ('a', 'aaaa', 'mx', 'txt', 'ns', 'soa')

    tasks = [
        asyncio.create_task(
            dns.asyncresolver.resolve(domain, record_type.capitalize())
        )
        for record_type in common_records
    ]

    result = await asyncio.gather(*tasks, return_exceptions=True)

    print([x for x in result])


def get_ip_info(ipaddress: str) -> IPInfo | IPError:
    params = {
        'lang': 'ru',
        'fields': ','.join(
            (
                'status',
                'message',
                'country',
                'countryCode',
                'regionName',
                'city',
                'lat',
                'lon',
                'timezone',
                'isp',
                'org',
                'reverse',
                'mobile',
                'proxy',
                'query',
                'as',
            )
        ),
    }

    with httpx.Client() as client:
        ipinfo = client.get(
            f'http://ip-api.com/json/{ipaddress}', params=params
        ).json()

    match ipinfo['status']:
        case 'success':
            ipinfo['asn'] = ipinfo['as']  # "as" can't be variable name
            ipinfo.pop('as')  # so remove it
            return IPInfo(**ipinfo)
        case 'fail':
            return IPError(**ipinfo)


if __name__ == '__main__':
    print(nslookup('ya.ru')[0])
