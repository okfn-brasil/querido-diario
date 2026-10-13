import asyncio
from datetime import date
from pathlib import Path
from urllib.parse import parse_qs

import pytest
from scrapy import Request
from scrapy.exceptions import DontCloseSpider, NotConfigured
from scrapy.http import HtmlResponse, TextResponse

from gazette.items import Gazette
from gazette.spiders.base.agape import BaseAgapeSpider

DATA_DIR = Path(__file__).parent / "data" / "agape"
PAGE_URL = "https://agportal.agapesistemas.com.br/DiarioOficial/?alias=pmtest"
ACTION_URL = (
    "https://agportal.agapesistemas.com.br/DiarioOficial/"
    "index.xhtml;jsessionid=TESTSESSION.aggr1no1"
)
SEARCH_BUTTON = "form:j_id35"


class AgapeSpiderForTest(BaseAgapeSpider):
    TERRITORY_ID = "0000000"
    name = "agape_test"
    alias = "pmtest"
    start_date = date(2026, 3, 1)


async def collect_start_requests(spider):
    return [request async for request in spider.start()]


def read_fixture(name):
    return (DATA_DIR / name).read_bytes()


def make_form_response(request=None):
    return HtmlResponse(
        url=PAGE_URL,
        body=read_fixture("form_page.html"),
        encoding="utf-8",
        request=request or Request(PAGE_URL, meta={"cookiejar": 2026}),
    )


def make_search_response(request):
    return TextResponse(
        url=request.url,
        body=read_fixture("search_response.xml"),
        encoding="utf-8",
        request=request,
    )


def get_search_request(spider, start=date(2026, 3, 1), end=date(2026, 3, 31)):
    response = make_form_response()
    requests = list(spider.search_request(response, start=start, end=end))
    assert len(requests) == 1
    return requests[0]


def get_body(request):
    # keep_blank_values: campos vazios do form (grupo, certificado...) são enviados
    return parse_qs(request.body.decode("utf-8"), keep_blank_values=True)


def test_missing_alias_is_not_configured():
    class SpiderWithoutAlias(BaseAgapeSpider):
        TERRITORY_ID = "0000000"
        name = "agape_without_alias"
        start_date = date(2026, 3, 1)

    with pytest.raises(NotConfigured):
        SpiderWithoutAlias()


def test_window_requests_builds_one_request_per_year_with_distinct_cookiejars():
    spider = AgapeSpiderForTest(start="2025-03-05", end="2026-10-12")

    start_requests = list(spider.window_requests())

    assert len(start_requests) == 2
    for request in start_requests:
        assert request.url == PAGE_URL
        assert request.callback == spider.search_request
        assert request.dont_filter
    assert start_requests[0].meta["cookiejar"] != start_requests[1].meta["cookiejar"]
    assert [request.cb_kwargs for request in start_requests] == [
        {"start": date(2025, 3, 5), "end": date(2025, 12, 31)},
        {"start": date(2026, 1, 1), "end": date(2026, 10, 12)},
    ]


def test_windows_cover_the_whole_interval_without_overlap():
    spider = AgapeSpiderForTest(start="2023-06-15", end="2026-02-20")

    start_requests = list(spider.window_requests())

    windows = [(r.cb_kwargs["start"], r.cb_kwargs["end"]) for r in start_requests]
    assert len(windows) == 4
    assert windows[0][0] == date(2023, 6, 15)
    assert windows[-1][1] == date(2026, 2, 20)
    for (_, previous_end), (next_start, _) in zip(windows, windows[1:]):
        assert next_start.year == previous_end.year + 1
        assert (previous_end, next_start) == (
            date(previous_end.year, 12, 31),
            date(previous_end.year + 1, 1, 1),
        )
    assert len({r.meta["cookiejar"] for r in start_requests}) == len(start_requests)


class FakeEngine:
    def __init__(self):
        self.crawled = []

    def crawl(self, request):
        self.crawled.append(request)


def test_start_yields_only_the_first_window():
    spider = AgapeSpiderForTest(start="2023-06-15", end="2026-02-20")

    start_requests = asyncio.run(collect_start_requests(spider))

    assert len(start_requests) == 1
    assert start_requests[0].cb_kwargs == {
        "start": date(2023, 6, 15),
        "end": date(2023, 12, 31),
    }


def test_spider_idle_schedules_the_remaining_windows_one_at_a_time():
    spider = AgapeSpiderForTest(start="2023-06-15", end="2026-02-20")
    spider.crawler = type("FakeCrawler", (), {"engine": FakeEngine()})()
    asyncio.run(collect_start_requests(spider))

    for expected_count in (1, 2, 3):
        with pytest.raises(DontCloseSpider):
            spider.spider_idle(spider)
        assert len(spider.crawler.engine.crawled) == expected_count

    # Sem janelas pendentes, o spider pode fechar
    spider.spider_idle(spider)
    crawled = spider.crawler.engine.crawled
    assert len(crawled) == 3
    assert [r.cb_kwargs["start"].year for r in crawled] == [2024, 2025, 2026]
    assert crawled[-1].cb_kwargs["end"] == date(2026, 2, 20)


def test_spider_idle_before_start_lets_the_spider_close():
    spider = AgapeSpiderForTest(start="2023-06-15", end="2026-02-20")

    assert spider.spider_idle(spider) is None


def test_start_within_a_single_year_builds_one_request():
    spider = AgapeSpiderForTest(start="2026-03-01", end="2026-03-31")

    start_requests = asyncio.run(collect_start_requests(spider))

    assert len(start_requests) == 1
    assert start_requests[0].cb_kwargs == {
        "start": date(2026, 3, 1),
        "end": date(2026, 3, 31),
    }


def test_search_request_builds_the_ajax_post():
    spider = AgapeSpiderForTest()

    request = get_search_request(spider)

    assert request.method == "POST"
    assert request.url == ACTION_URL
    assert request.meta["cookiejar"] == 2026
    body = get_body(request)
    assert body["AJAXREQUEST"] == ["_viewRoot"]
    assert body[SEARCH_BUTTON] == [SEARCH_BUTTON]
    assert body["form:entidade"] == ["1"]
    assert body["form:de"] == ["01/03/2026"]
    assert body["form:ate"] == ["31/03/2026"]
    # campos que o portal exige no postback
    assert body["form"] == ["form"]
    assert body["javax.faces.ViewState"] == ["j_id1"]
    assert request.cb_kwargs["form_response"].url == PAGE_URL
    assert request.cb_kwargs["formdata"]["form:de"] == "01/03/2026"


def test_search_request_keeps_the_cookiejar_of_the_start_request():
    spider = AgapeSpiderForTest()
    form_response = make_form_response(Request(PAGE_URL, meta={"cookiejar": 2025}))

    (request,) = spider.search_request(
        form_response, start=date(2025, 1, 1), end=date(2025, 12, 31)
    )

    assert request.meta["cookiejar"] == 2025
    assert get_body(request)["form:de"] == ["01/01/2025"]
    assert get_body(request)["form:ate"] == ["31/12/2025"]


def test_search_request_picks_the_option_with_prefeitura_in_the_description():
    spider = AgapeSpiderForTest()
    page = read_fixture("form_page.html").decode("utf-8")
    page = page.replace(
        '<option value="1">PREFEITURA',
        '<option value="7">CAMARA MUNICIPAL DE TESTE</option>'
        '<option value="9">Prefeitura de teste</option>'
        '<option value="1">PREFEITURA',
    )
    response = HtmlResponse(
        url=PAGE_URL,
        body=page.encode("utf-8"),
        encoding="utf-8",
        request=Request(PAGE_URL, meta={"cookiejar": 2026}),
    )

    (request,) = spider.search_request(
        response, start=date(2026, 3, 1), end=date(2026, 3, 31)
    )

    assert get_body(request)["form:entidade"] == ["9"]


def test_search_request_uses_the_entity_attribute_when_defined():
    class SpiderWithEntity(AgapeSpiderForTest):
        entity = "7"

    request = get_search_request(SpiderWithEntity())

    assert get_body(request)["form:entidade"] == ["7"]


def test_search_request_fails_when_there_is_no_city_hall_option():
    spider = AgapeSpiderForTest()
    page = read_fixture("form_page.html").decode("utf-8")
    page = page.replace("PREFEITURA MUNICIPAL", "CAMARA MUNICIPAL")
    response = HtmlResponse(
        url=PAGE_URL,
        body=page.encode("utf-8"),
        encoding="utf-8",
        request=Request(PAGE_URL, meta={"cookiejar": 2026}),
    )

    with pytest.raises(NotConfigured):
        list(
            spider.search_request(
                response, start=date(2026, 3, 1), end=date(2026, 3, 31)
            )
        )


def parse_search_response(spider):
    search_request = get_search_request(spider)
    response = make_search_response(search_request)
    return list(spider.parse(response, **search_request.cb_kwargs))


def test_parse_yields_one_gazette_per_edition_ignoring_standalone_acts():
    spider = AgapeSpiderForTest()

    gazettes = parse_search_response(spider)

    # a fixture tem 3 edições (índices 0, 1 e 10) e 5 atos avulsos (":j_id80")
    assert all(isinstance(gazette, Gazette) for gazette in gazettes)
    assert [(g["date"], g["edition_number"]) for g in gazettes] == [
        (date(2026, 3, 5), "1"),
        (date(2026, 3, 16), "2"),
        (date(2026, 3, 31), "11"),
    ]
    for gazette in gazettes:
        assert gazette["is_extra_edition"] is False
        assert gazette["power"] == "executive"
        assert len(gazette["file_requests"]) == 1


def test_parse_builds_a_download_postback_for_each_edition():
    spider = AgapeSpiderForTest()

    gazettes = parse_search_response(spider)

    expected_link_ids = [
        "form:j_id55:0:j_id60:0:j_id65:0:j_id73",
        "form:j_id55:0:j_id60:0:j_id65:1:j_id73",
        "form:j_id55:0:j_id60:0:j_id65:10:j_id73",
    ]
    for gazette, link_id in zip(gazettes, expected_link_ids):
        request = gazette["file_requests"][0]
        body = get_body(request)
        assert request.method == "POST"
        assert request.meta["cookiejar"] == 2026
        assert body[link_id] == [link_id]
        assert "AJAXREQUEST" not in body
        # nenhum outro link (de outra edição ou ato avulso) vai no corpo
        assert [key for key in body if key.endswith((":j_id73", ":j_id80"))] == [
            link_id
        ]
        # o download reenvia os mesmos filtros da busca
        assert body["form:entidade"] == ["1"]
        assert body["form:de"] == ["01/03/2026"]
        assert body["form:ate"] == ["31/03/2026"]
        assert body["javax.faces.ViewState"] == ["j_id1"]


def test_parse_download_postback_does_not_include_the_search_button():
    spider = AgapeSpiderForTest()

    gazettes = parse_search_response(spider)

    for gazette in gazettes:
        assert SEARCH_BUTTON not in get_body(gazette["file_requests"][0])


def test_parse_builds_unique_pdf_urls_for_the_files_pipeline():
    spider = AgapeSpiderForTest()

    gazettes = parse_search_response(spider)

    urls = [gazette["file_requests"][0].url for gazette in gazettes]
    assert urls == [
        f"{ACTION_URL}?data=2026-03-05&edicao=1&arquivo=diario.pdf",
        f"{ACTION_URL}?data=2026-03-16&edicao=2&arquivo=diario.pdf",
        f"{ACTION_URL}?data=2026-03-31&edicao=11&arquivo=diario.pdf",
    ]
    assert len(set(urls)) == len(urls)
    assert all(url.endswith("arquivo=diario.pdf") for url in urls)


def test_parse_keeps_the_cookiejar_of_the_search_response():
    spider = AgapeSpiderForTest()
    form_response = make_form_response(Request(PAGE_URL, meta={"cookiejar": 2024}))
    (search_request,) = spider.search_request(
        form_response, start=date(2024, 1, 1), end=date(2024, 12, 31)
    )

    gazettes = list(
        spider.parse(make_search_response(search_request), **search_request.cb_kwargs)
    )

    assert len(gazettes) == 3
    assert {g["file_requests"][0].meta["cookiejar"] for g in gazettes} == {2024}


def test_parse_without_results_yields_nothing():
    spider = AgapeSpiderForTest()
    search_request = get_search_request(spider)
    response = TextResponse(
        url=search_request.url,
        body=b'<?xml version="1.0"?><html><body><div id="form:publicacoes">'
        b"<h4>Resultado da busca:</h4></div></body></html>",
        encoding="utf-8",
        request=search_request,
    )

    assert list(spider.parse(response, **search_request.cb_kwargs)) == []


def test_parse_download_requests_expect_a_file_content_type():
    spider = AgapeSpiderForTest()

    gazettes = parse_search_response(spider)

    for gazette in gazettes:
        meta = gazette["file_requests"][0].meta
        assert meta["expected_content_types"] == spider.FILE_CONTENT_TYPES
