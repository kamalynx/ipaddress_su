import asyncio
import logging

import dns.asyncresolver
import dns.resolver


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


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

    return result


async def get_dns_records(domain):
    common_records = ('a', 'aaaa', 'mx', 'txt', 'ns', 'soa')

    tasks = [
        asyncio.create_task(dns.asyncresolver.resolve(domain, record_type.capitalize()))
        for record_type in common_records
    ]

    result = await asyncio.gather(*tasks, return_exceptions=True)

    print([x for x in result])


if __name__ == '__main__':
    asyncio.run(get_dns_records('kamafish.ru'))
