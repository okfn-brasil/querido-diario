import asyncio
import json
from datetime import date

import pytest
from scrapy.exceptions import NotConfigured
from scrapy.http import TextResponse

from gazette.items import Gazette
from gazette.spiders.base.eatos import BaseEatosSpider

API = "https://api.publicacoesmunicipais.com.br/api"


class EatosSpiderForTest(BaseEatosSpider):
    TERRITORY_ID = "0000000"
    name = "eatos_test"
    url_path = "cidade"
    start_date = date(2026, 1, 1)


def make_act(edition, date_text):
    return {"edition": edition, "date": date_text, "entityPath": "cidade"}


def make_response(acts, total, page=1):
    return TextResponse(
        url=f"{API}/v1/acts?page={page}&pageSize=100&urlPath=cidade",
        body=json.dumps({"acts": acts, "total": total}).encode("utf-8"),
        encoding="utf-8",
    )


async def collect_start_requests(spider):
    return [request async for request in spider.start()]


def test_url_path_is_required():
    class SpiderWithoutUrlPath(BaseEatosSpider):
        TERRITORY_ID = "0000000"
        name = "eatos_without_url_path"
        start_date = date(2026, 1, 1)

    with pytest.raises(NotConfigured):
        SpiderWithoutUrlPath()


def test_start_requests_the_first_page():
    spider = EatosSpiderForTest()

    requests = asyncio.run(collect_start_requests(spider))

    assert len(requests) == 1
    assert requests[0].url == f"{API}/v1/acts?page=1&pageSize=100&urlPath=cidade"
    assert requests[0].cb_kwargs == {"page": 1}


def test_parse_builds_gazettes_with_the_pdf_url():
    spider = EatosSpiderForTest(end="2026-12-31")
    acts = [
        make_act("3389", "2026-11-09T14:58:24.413295-03:00"),
        make_act("3388", "2026-11-06T09:01:02.5-03:00"),
    ]

    results = list(spider.parse(make_response(acts, total=2), page=1))

    assert all(isinstance(item, Gazette) for item in results)
    assert [item["edition_number"] for item in results] == ["3389", "3388"]
    assert results[0]["date"] == date(2026, 11, 9)
    assert results[0]["file_urls"] == [f"{API}/v2/acts/cidade/3389"]
    assert results[0]["is_extra_edition"] is False
    assert results[0]["power"] == "executive"


def test_parse_requests_the_next_page_while_inside_the_interval():
    spider = EatosSpiderForTest(end="2026-12-31")
    acts = [make_act("10", "2026-03-02T10:00:00-03:00")]

    results = list(spider.parse(make_response(acts, total=250), page=1))

    next_page = results[-1]
    assert next_page.url == f"{API}/v1/acts?page=2&pageSize=100&urlPath=cidade"
    assert next_page.cb_kwargs == {"page": 2}


def test_parse_stops_after_passing_the_start_date():
    spider = EatosSpiderForTest(start="2026-03-01", end="2026-12-31")
    acts = [
        make_act("10", "2026-03-02T10:00:00-03:00"),
        make_act("9", "2026-02-27T10:00:00-03:00"),
    ]

    results = list(spider.parse(make_response(acts, total=250), page=1))

    assert [item["edition_number"] for item in results] == ["10"]


def test_parse_skips_editions_after_the_end_date():
    spider = EatosSpiderForTest(start="2026-01-01", end="2026-03-01")
    acts = [
        make_act("10", "2026-03-02T10:00:00-03:00"),
        make_act("9", "2026-02-27T10:00:00-03:00"),
    ]

    results = list(spider.parse(make_response(acts, total=2), page=1))

    assert [item["edition_number"] for item in results] == ["9"]


def test_parse_stops_on_the_last_page():
    spider = EatosSpiderForTest(end="2026-12-31")
    acts = [make_act("10", "2026-03-02T10:00:00-03:00")]

    results = list(spider.parse(make_response(acts, total=201, page=3), page=3))

    assert [type(item) for item in results] == [Gazette]


def test_parse_handles_a_page_without_acts():
    spider = EatosSpiderForTest(end="2026-12-31")

    results = list(spider.parse(make_response([], total=0), page=1))

    assert results == []
