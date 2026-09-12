import asyncio
import json
from datetime import date

from scrapy.http import TextResponse

from gazette.spiders.rj.rj_itaguai import RjItaguaiSpider


async def collect_start_requests(spider):
    return [request async for request in spider.start()]


def make_response(payload):
    return TextResponse(
        url=RjItaguaiSpider.editions_url,
        body=json.dumps(payload).encode("utf-8"),
        encoding="utf-8",
    )


def test_start_requests_the_attos_editions_index():
    spider = RjItaguaiSpider()

    start_requests = asyncio.run(collect_start_requests(spider))

    assert len(start_requests) == 1
    assert start_requests[0].url == RjItaguaiSpider.editions_url


def test_parse_emits_editions_in_the_requested_period():
    spider = RjItaguaiSpider(start="2026-09-01", end="2026-09-12")
    payload = [
        {
            "numero": 1515,
            "nome": "Edição nº 1515 — 11/09/2026",
            "data": "2026-09-11",
            "arquivo": "/api/pdf?id=edition-1515&n=1515",
        },
        {
            "numero": 1510,
            "nome": "Edição nº 1510 — 28/08/2026",
            "data": "2026-08-28",
            "arquivo": "/api/pdf?id=edition-1510&n=1510",
        },
        {
            "numero": 780,
            "nome": "Edição nº 780",
            "data": None,
            "arquivo": "/api/pdf?id=edition-780&n=780",
        },
    ]

    gazettes = list(spider.parse(make_response(payload)))

    assert len(gazettes) == 1
    assert gazettes[0]["date"] == date(2026, 9, 11)
    assert gazettes[0]["edition_number"] == "1515"
    assert gazettes[0]["file_urls"] == [
        "https://www.attosoficiais.com.br/api/pdf?id=edition-1515&n=1515"
    ]
