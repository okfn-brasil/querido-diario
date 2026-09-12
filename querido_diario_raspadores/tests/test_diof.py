import asyncio
import json
from datetime import date

from scrapy.http import TextResponse

from gazette.spiders.base.diof import BaseDiofSpider
from gazette.utils.dates import DateRange


class DiofSpiderForTest(BaseDiofSpider):
    TERRITORY_ID = "0000000"
    name = "diof_test"
    website = "https://example.com"
    start_date = date(2026, 1, 1)
    power = "executive"


async def collect_start_requests(spider):
    return [request async for request in spider.start()]


def make_response(
    payload, url="https://diof.io.org.br/api/diario-oficial/edicoes-anteriores-group"
):
    return TextResponse(
        url=url,
        body=json.dumps(payload).encode("utf-8"),
        encoding="utf-8",
    )


def test_start_builds_client_info_request():
    spider = DiofSpiderForTest()

    start_requests = asyncio.run(collect_start_requests(spider))

    assert len(start_requests) == 1
    assert start_requests[0].url.endswith("/dados-cliente/info/")
    assert start_requests[0].headers["Origin"] == b"https://example.com"
    assert start_requests[0].callback == spider.interval_request


def test_parse_items_unwraps_the_data_envelope():
    # A API passou a envelopar a lista de datas num objeto
    # {"data": [...], "page", "pages", "count"} em vez de retornar a lista
    # diretamente.
    spider = DiofSpiderForTest()
    spider.client_id = "123"
    interval = DateRange(start=date(2026, 9, 1), end=date(2026, 9, 12))
    payload = {
        "data": [
            {
                "key": "2026-09-10T00:00:00",
                "elements": [
                    {
                        "cod_documento": 42,
                        "dat_envio": "2026-09-10T14:14:13",
                        "des_arquivoa4": "some_file_id",
                    }
                ],
            }
        ],
        "page": 1,
        "pages": 1,
        "count": 1,
    }

    requests = list(
        spider.parse_items(make_response(payload), interval=interval, page=1)
    )

    assert len(requests) == 1
    gazette_request = requests[0]
    assert gazette_request.url.endswith("/diario-oficial/download/some_file_id.pdf")
    assert gazette_request.cb_kwargs["metadata"]["edition_number"] == "42"
    assert gazette_request.cb_kwargs["metadata"]["date"] == date(2026, 9, 10)


def test_parse_items_requests_the_next_page_when_there_is_one():
    spider = DiofSpiderForTest()
    spider.client_id = "123"
    interval = DateRange(start=date(2026, 8, 1), end=date(2026, 9, 12))
    payload = {"data": [], "page": 1, "pages": 3, "count": 15}

    results = list(
        spider.parse_items(make_response(payload), interval=interval, page=1)
    )

    assert len(results) == 1
    next_page_request = results[0]
    assert next_page_request.callback == spider.parse_items
    assert next_page_request.cb_kwargs == {"interval": interval, "page": 2}
    assert json.loads(next_page_request.body)["page"] == 2


def test_parse_items_stops_on_the_last_page():
    spider = DiofSpiderForTest()
    spider.client_id = "123"
    interval = DateRange(start=date(2026, 8, 1), end=date(2026, 9, 12))
    payload = {"data": [], "page": 3, "pages": 3, "count": 15}

    results = list(
        spider.parse_items(make_response(payload), interval=interval, page=3)
    )

    assert results == []


def test_parse_items_treats_missing_pages_field_as_single_page():
    # respostas antigas (ou mocks incompletos) podem não ter o campo
    # "pages" — não deve tentar paginar indefinidamente nesse caso.
    spider = DiofSpiderForTest()
    spider.client_id = "123"
    interval = DateRange(start=date(2026, 8, 1), end=date(2026, 9, 12))
    payload = {"data": []}

    results = list(
        spider.parse_items(make_response(payload), interval=interval, page=1)
    )

    assert results == []
