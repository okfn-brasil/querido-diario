from datetime import date

from scrapy.http import TextResponse

from gazette.spiders.base.adiarios_v2 import BaseAdiariosV2Spider


class AdiariosV2SpiderForTest(BaseAdiariosV2Spider):
    BASE_URL = "https://example.com"
    TERRITORY_ID = "0000000"
    allowed_domains = ["example.com"]
    name = "adiarios_v2_test"
    start_date = date(2026, 1, 1)


def make_response(body):
    return TextResponse(
        url="https://example.com/jornal.php",
        body=body.encode("utf-8"),
        encoding="utf-8",
    )


def test_get_last_page_number_assumes_one_page_without_pagination():
    spider = AdiariosV2SpiderForTest()

    assert spider.get_last_page_number(make_response("<table></table>")) == 1


def test_get_last_page_number_ignores_non_numeric_pagination_labels():
    spider = AdiariosV2SpiderForTest()
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
