from datetime import date

from scrapy.http import TextResponse

from gazette.spiders.base.aratext import BaseAratextSpider


class AratextSpiderForTest(BaseAratextSpider):
    TERRITORY_ID = "0000000"
    name = "aratext_test"
    power = "executive"
    start_date = date(2026, 1, 1)
    start_urls = ["https://example.com/diariooficial"]


def make_response(body):
    return TextResponse(
        url="https://example.com/diariooficial",
        body=body.encode("utf-8"),
        encoding="utf-8",
    )


def test_parse_stops_without_error_when_an_empty_page_has_no_next_link():
    spider = AratextSpiderForTest(end="2026-09-12")
    response = make_response("<table id='edicoes-anteriores'><tbody></tbody></table>")

    assert list(spider.parse(response)) == []


def test_parse_requests_next_page_when_an_empty_page_has_a_next_link():
    spider = AratextSpiderForTest(end="2026-09-12")
    response = make_response(
        """
        <table id="edicoes-anteriores"><tbody></tbody></table>
        <div class="pagination"><a rel="next" href="?page=2">Próxima</a></div>
        """
    )

    requests = list(spider.parse(response))

    assert len(requests) == 1
    assert requests[0].url == "https://example.com/diariooficial?page=2"
    assert requests[0].cb_kwargs == {"page": 2}
