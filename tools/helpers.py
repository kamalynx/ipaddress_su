import asyncio
import logging
from io import BytesIO
from collections.abc import Iterable

import dns.asyncresolver
import dns.resolver
import httpx
from attrs import define
from playwright.async_api import async_playwright


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


def do_nslookup(domain):
    ipsv4 = None
    ipsv6 = None

    try:
        ipsv4 = dns.resolver.resolve(domain, "a")
        ipsv6 = dns.resolver.resolve(domain, "aaaa")
    except dns.resolver.NoAnswer as err:
        logger.error(err)

    return ipsv4, ipsv6


async def a_do_nslookup(domain):
    tasks = [
        asyncio.create_task(dns.asyncresolver.resolve(domain, "a")),
        asyncio.create_task(dns.asyncresolver.resolve(domain, "aaaa")),
    ]

    result = await asyncio.gather(*tasks, return_exceptions=True)

    for i in result:
        print(isinstance(i, Iterable))

    return result


async def get_dns_records(domain):
    common_records = ('a', 'aaaa', 'mx', 'txt', 'ns', 'soa')

    tasks = [
        asyncio.create_task(dns.asyncresolver.resolve(domain, record_type.capitalize()))
        for record_type in common_records
    ]

    result = await asyncio.gather(*tasks, return_exceptions=True)

    print([x for x in result])


async def take_screenshot(url: str) -> bytes:
    async with async_playwright() as pw:
        browser = await pw.firefox.launch()
        page = await browser.new_page()
        await page.goto(url)
        scr = await page.screenshot(scale='css')
        return BytesIO(scr)


def get_ip_info(ipaddress: str):
    params = {
        'lang': 'ru',
        'fields': ','.join((
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
        )),
    }

    with httpx.Client() as client:
        result = client.get(f'http://ip-api.com/json/{ipaddress}', params=params)

    return IPInfo(**result.json())


if __name__ == '__main__':
    # ~ asyncio.run(get_dns_records('kamafish.ru'))
    # ~ print(asyncio.run(take_screenshot('https://ipaddress.su')))
    print(get_ip_info('212.33.245.31'))
