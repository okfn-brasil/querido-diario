import asyncio
from datetime import date
from pathlib import Path

from scrapy.http import TextResponse

from gazette.spiders.es.es_estado import EsEstadoSpider

FIXTURES_DIR = Path(__file__).parent / "fixtures" / "es_estado"
LISTING_URL = (
    "https://ioes.dio.es.gov.br/apifront/portal/edicoes/edicoes_from_data/{}.json"
)


async def collect_start_requests(spider):
    return [request async for request in spider.start()]


def parse_fixture(spider, day):
    response = TextResponse(
        url=LISTING_URL.format(day.isoformat()),
        body=(FIXTURES_DIR / f"{day.isoformat()}.json").read_bytes(),
        encoding="utf-8",
    )
    return list(spider.parse(response, gazette_date=day))


def test_start_requests_one_state_listing_per_day():
    spider = EsEstadoSpider(start="2026-10-08", end="2026-10-10")

    start_requests = asyncio.run(collect_start_requests(spider))

    # Sem `?subtheme=`, a API devolve só o diário estadual; os subtemas
    # (diariodaserra, dom, caderno_municipios) são diários municipais.
    assert [request.url for request in start_requests] == [
        LISTING_URL.format("2026-10-08"),
        LISTING_URL.format("2026-10-09"),
        LISTING_URL.format("2026-10-10"),
    ]
    assert all("subtheme" not in request.url for request in start_requests)
    assert start_requests[0].cb_kwargs == {"gazette_date": date(2026, 10, 8)}


def test_spider_follows_collection_decisions():
    spider = EsEstadoSpider()

    assert spider.TERRITORY_ID == "3299999"
    assert spider.allowed_domains == ["ioes.dio.es.gov.br"]
    assert spider.start_date == date(2003, 3, 17)
    assert spider.custom_settings["DOWNLOAD_DELAY"] == 0.5


def test_parse_yields_one_gazette_per_edition():
    spider = EsEstadoSpider()

    gazettes = parse_fixture(spider, date(2026, 10, 8))

    assert len(gazettes) == 2
    extra, regular = gazettes

    assert dict(extra) == {
        "date": date(2026, 10, 8),
        "edition_number": 26826,
        "is_extra_edition": True,
        "file_urls": ["https://ioes.dio.es.gov.br/portal/edicoes/download/11538"],
        "power": "executive",
    }
    assert dict(regular) == {
        "date": date(2026, 10, 8),
        "edition_number": 26826,
        "is_extra_edition": False,
        "file_urls": ["https://ioes.dio.es.gov.br/portal/edicoes/download/11533"],
        "power": "executive",
    }


def test_parse_omits_edition_number_when_listing_reports_zero():
    spider = EsEstadoSpider()

    gazettes = parse_fixture(spider, date(2014, 1, 2))

    assert len(gazettes) == 1
    assert "edition_number" not in gazettes[0]
    assert gazettes[0]["file_urls"] == [
        "https://ioes.dio.es.gov.br/portal/edicoes/download/1849"
    ]


def test_parse_ignores_day_without_edition():
    spider = EsEstadoSpider()

    assert parse_fixture(spider, date(2026, 10, 10)) == []
