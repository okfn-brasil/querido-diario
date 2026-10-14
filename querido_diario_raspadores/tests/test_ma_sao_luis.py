import asyncio
import json
from datetime import date

from scrapy import Request
from scrapy.http import TextResponse

from gazette.spiders.ma.ma_sao_luis import MASaoLuisSpider


async def collect_start_requests(spider):
    return [request async for request in spider.start()]


def make_response(payload, page=1):
    return TextResponse(
        url=f"{MASaoLuisSpider.archive_url}?page={page}&limit=200",
        body=json.dumps(payload).encode("utf-8"),
        encoding="utf-8",
    )


def make_edition(edition_date, name, url):
    return {
        "edition_date": f"{edition_date}T00:00:00.000Z",
        "edition_number": name,
        "pdf_download_url": url,
    }


def test_start_requests_the_first_archive_page():
    spider = MASaoLuisSpider()

    start_requests = asyncio.run(collect_start_requests(spider))

    assert len(start_requests) == 1
    assert start_requests[0].url == f"{MASaoLuisSpider.archive_url}?page=1&limit=200"
    assert start_requests[0].cb_kwargs == {"page": 1}


def test_parse_emits_editions_in_the_requested_period():
    spider = MASaoLuisSpider(start="2026-10-01", end="2026-10-08")
    payload = {
        "total_pages": 1,
        "editions": [
            make_edition("2026-10-09", "Edição nº 238/XLVI", "/api/editions/140/pdf"),
            make_edition(
                "2026-10-07", "Edição nº 236/XLVI EXTRA", "/api/editions/138/pdf"
            ),
            make_edition("2026-10-07", "Edição nº 235/XLVI", "/api/editions/137/pdf"),
            make_edition("2026-09-30", "Edição nº 229/XLVI", "/uploads/229.pdf"),
        ],
    }

    gazettes = list(spider.parse(make_response(payload), page=1))

    assert [
        (g["date"], g["edition_number"], g["is_extra_edition"]) for g in gazettes
    ] == [
        (date(2026, 10, 7), "236", True),
        (date(2026, 10, 7), "235", False),
    ]
    assert gazettes[0]["file_urls"] == [
        "https://diariooficial.saoluis.ma.gov.br/api/editions/138/pdf"
    ]
    assert gazettes[0]["power"] == "executive_legislative"


def test_parse_requests_next_page_until_start_date():
    spider = MASaoLuisSpider(start="2026-09-01")
    payload = {
        "total_pages": 52,
        "editions": [
            make_edition("2026-09-15", "Edição nº 220/XLVI", "/uploads/220.pdf"),
        ],
    }

    results = list(spider.parse(make_response(payload), page=1))

    next_requests = [r for r in results if isinstance(r, Request)]
    assert len(next_requests) == 1
    assert next_requests[0].url == f"{MASaoLuisSpider.archive_url}?page=2&limit=200"
    assert next_requests[0].cb_kwargs == {"page": 2}


def test_parse_stops_after_start_date_or_last_page():
    spider = MASaoLuisSpider(start="2026-09-01")
    older = {
        "total_pages": 52,
        "editions": [
            make_edition("2026-08-31", "Edição nº 200/XLVI", "/uploads/200.pdf"),
        ],
    }
    last = {
        "total_pages": 52,
        "editions": [
            make_edition("2026-09-02", "Edição nº 201/XLVI", "/uploads/201.pdf"),
        ],
    }

    assert not any(
        isinstance(r, Request) for r in spider.parse(make_response(older), 3)
    )
    assert not any(
        isinstance(r, Request) for r in spider.parse(make_response(last), 52)
    )


def test_edition_number_formats_of_the_archive():
    cases = {
        "Edição nº 238/XLVI": "238",
        "diario_oficial_038_XLVI.pdf": "38",
        "dom-prefeitura-municipal-de-sao-luis-ano-xliv-edicao-0597-assinado.pdf": "597",
        "DOM-2015-142-S-A123.pdf": "142",
        "DIÁRIO OFICIAL - Nº 19 - 1981.pdf": "19",
        "diario.pdf": "",
    }

    for name, number in cases.items():
        assert MASaoLuisSpider._edition_number(name) == number


def test_supplements_are_extra_editions():
    assert MASaoLuisSpider._is_extra_edition("DOM-2015-142-S-A123.pdf")
    assert not MASaoLuisSpider._is_extra_edition("DOM-2015-142-N-FE37.pdf")
    assert MASaoLuisSpider._is_extra_edition("Edição nº 230/XLVI Extra")
