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
