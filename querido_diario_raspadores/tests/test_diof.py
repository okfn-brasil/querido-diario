import asyncio
from datetime import date

from gazette.spiders.base.diof import BaseDiofSpider


class DiofSpiderForTest(BaseDiofSpider):
    TERRITORY_ID = "0000000"
    name = "diof_test"
    website = "https://example.com"
    start_date = date(2026, 1, 1)
    power = "executive"


async def collect_start_requests(spider):
    return [request async for request in spider.start()]


def test_start_builds_client_info_request():
    spider = DiofSpiderForTest()

    start_requests = asyncio.run(collect_start_requests(spider))

    assert len(start_requests) == 1
    assert start_requests[0].url.endswith("/dados-cliente/info/")
    assert start_requests[0].headers["Origin"] == b"https://example.com"
    assert start_requests[0].callback == spider.interval_request
