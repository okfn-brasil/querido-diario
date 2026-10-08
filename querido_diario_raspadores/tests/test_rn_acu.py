import asyncio
from datetime import date

from scrapy import Request
from scrapy.http import HtmlResponse

from gazette.items import Gazette
from gazette.spiders.rn.rn_acu import RnAcuSpider

BASE_URL = "https://assu.rn.gov.br/diario_oficial/"


async def collect_start_requests(spider):
    return [request async for request in spider.start()]


def make_item(number, title, listed_date, file_url):
    fields = "".join(
        f'<div class="jet-listing-dynamic-field__content">{value}</div>'
        for value in (number, title, listed_date)
    )
    link = f'<a href="{file_url}">Baixar</a>' if file_url else ""
    return f'<div class="jet-listing-grid__item">{fields}{link}</div>'


def make_response(url, items, page=1, pages=124):
    body = f"""
    <html><body>
        <div id="busca_dom">
            <div class="jet-listing-grid__items" data-page="{page}" data-pages="{pages}">
                {''.join(items)}
            </div>
        </div>
    </body></html>
    """
    return HtmlResponse(url=url, body=body.encode("utf-8"), encoding="utf-8")


def split_results(results):
    gazettes = [result for result in results if isinstance(result, Gazette)]
    requests = [result for result in results if isinstance(result, Request)]
    return gazettes, requests


def test_start_requests_the_editions_listing():
    spider = RnAcuSpider()

    requests = asyncio.run(collect_start_requests(spider))

    assert [request.url for request in requests] == [BASE_URL]


def test_parse_editions_in_the_requested_period_and_stop_pagination():
    spider = RnAcuSpider(start="2026-10-01", end="2026-10-05")
    response = make_response(
        BASE_URL,
        [
            make_item(
                "5461",
                "EDIÇÃO ANO XXII – N° 5461 - TERÇA-FEIRA, 06 DE OUTUBRO DE 2026",
                "06/10/2026",
                "https://drive.google.com/file/d/19ArAVIgXgBjRJTN6I0iASH7WJ6yl8yri/view?usp=drive_link",
            ),
            make_item(
                "SEXTA",
                "EDIÇÃO ANO XXII – N° 5459 - SEXTA-FEIRA, 02 DE OUTUBRO DE 2026",
                "02/10/2026",
                "https://drive.google.com/file/d/1KpsdzEq0oZN6_m5wY5qvHofytnGUVUTN/view?usp=drive_link",
            ),
            make_item(
                "5457",
                "EDIÇÃO EXTRAORDINÁRIA ANO XXII – N° 5457 - QUARTA-FEIRA, 30 DE SETEMBRO DE 2026",
                "30/09/2026",
                "https://drive.google.com/file/d/1naYY01hpy_9usLGeuLjfeyqREfEDgTcX/view?usp=drive_link",
            ),
        ],
    )

    gazettes, requests = split_results(list(spider.parse(response)))

    assert len(gazettes) == 1
    assert gazettes[0]["date"] == date(2026, 10, 2)
    assert gazettes[0]["edition_number"] == "5459"
    assert gazettes[0]["is_extra_edition"] is False
    assert gazettes[0]["power"] == "executive_legislative"
    assert gazettes[0]["file_urls"] == [
        "https://drive.google.com/uc?export=download&id=1KpsdzEq0oZN6_m5wY5qvHofytnGUVUTN"
    ]
    assert requests == []


def test_parse_prefers_the_date_in_the_title_and_follows_next_page():
    spider = RnAcuSpider(start="2013-01-01", end="2013-12-31")
    response = make_response(
        f"{BASE_URL}?jsf=jet-engine:busca_dom&pagenum=123",
        [
            make_item(
                "2099",
                "EDIÇÃO ANO IX – N° 2099 – terça-feira, 08 de janeiro de 2013",
                "18/09/2013",
                "https://drive.google.com/file/d/1Lwy2QCq9d32WTOyPSJ_Bi2FQSm1hA8Ui/view?usp=drive_link",
            ),
            make_item(
                "2098",
                "EDIÇÃO EXTRA ANO IX – N° 2098 – sexta-feira, 04 de janeiro de 2013",
                "04/01/2013",
                None,
            ),
        ],
        page=123,
    )

    gazettes, requests = split_results(list(spider.parse(response, page=123)))

    assert len(gazettes) == 1
    assert gazettes[0]["date"] == date(2013, 1, 8)
    assert gazettes[0]["edition_number"] == "2099"
    assert [request.url for request in requests] == [
        f"{BASE_URL}?jsf=jet-engine:busca_dom&pagenum=124"
    ]
    assert requests[0].cb_kwargs == {"page": 124}
