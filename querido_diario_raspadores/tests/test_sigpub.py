import asyncio
from datetime import date

from gazette.spiders.base.sigpub import BaseSigpubSpider


class SigpubSpiderForTest(BaseSigpubSpider):
    CALENDAR_URL = "https://example.com/calendar"
    TERRITORY_ID = "0000000"
    name = "sigpub_test"
    start_date = date(2026, 1, 1)


async def collect_start_requests(spider):
    return [request async for request in spider.start()]


def test_start_delegates_to_legacy_start_requests():
    spider = SigpubSpiderForTest()

    legacy_requests = list(spider.start_requests())
    start_requests = asyncio.run(collect_start_requests(spider))

    assert len(start_requests) == len(legacy_requests) == 1
    assert start_requests[0].url == legacy_requests[0].url
    assert start_requests[0].callback == legacy_requests[0].callback
