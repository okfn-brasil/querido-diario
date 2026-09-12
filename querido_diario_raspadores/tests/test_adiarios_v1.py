from datetime import date

from scrapy.http import TextResponse

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class AdiariosV1SpiderForTest(BaseAdiariosV1Spider):
    BASE_URL = "https://example.com"
    TERRITORY_ID = "0000000"
    allowed_domains = ["example.com"]
    name = "adiarios_v1_test"
    start_date = date(2026, 1, 1)


def make_response(body):
    return TextResponse(
        url="https://example.com/diariooficial.php",
        body=body.encode("utf-8"),
        encoding="utf-8",
    )


def test_get_last_page_number_assumes_one_page_without_pagination():
    spider = AdiariosV1SpiderForTest()

    assert (
        spider.get_last_page_number(make_response("<div id='diario_lista'></div>")) == 1
    )


def test_get_last_page_number_ignores_non_numeric_pagination_labels():
    spider = AdiariosV1SpiderForTest()
    response = make_response(
        """
        <ul class="pagination">
          <li><a><span>1</span></a></li>
          <li><a><span>...</span></a></li>
          <li><a><span>3</span></a></li>
        </ul>
        """
    )

    assert spider.get_last_page_number(response) == 3
