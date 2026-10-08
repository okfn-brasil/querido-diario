import asyncio
from datetime import date

from scrapy import Request
from scrapy.http import HtmlResponse

from gazette.items import Gazette
from gazette.spiders.rn.rn_extremoz import RnExtremozSpider

BASE_URL = "https://extremoz.rn.gov.br/diario-oficial"


async def collect_start_requests(spider):
    return [request async for request in spider.start()]


def make_item(title, listed_date, file_url):
    link = f'<a href="{file_url}" target="_blank">' if file_url else "<a>"
    return f"""
    <article class="arq-list-item contrast">
        <div class="arq-list-item-content">
            {link}
                <h1>{title}</h1>
                <p class="data"><i class="sogo_icon-calendar-services"></i> {listed_date}</p>
            </a>
        </div>
    </article>
    """


def make_response(url, items, next_page_url=None):
    pagination = (
        f'<a class="next page-numbers" href="{next_page_url}">próxima</a>'
        if next_page_url
        else ""
    )
    body = f"<html><body>{''.join(items)}{pagination}</body></html>"
    return HtmlResponse(url=url, body=body.encode("utf-8"), encoding="utf-8")


def split_results(results):
    gazettes = [result for result in results if isinstance(result, Gazette)]
    requests = [result for result in results if isinstance(result, Request)]
    return gazettes, requests


def test_start_requests_yearly_pages_in_the_requested_period():
    spider = RnExtremozSpider(start="2025-12-20", end="2026-01-10")

    requests = asyncio.run(collect_start_requests(spider))

    assert [request.url for request in requests] == [
        f"{BASE_URL}/diario-oficial-2025/",
        f"{BASE_URL}/diario-oficial-2026/",
    ]


def test_start_requests_include_previous_years_page_before_2014():
    spider = RnExtremozSpider(start="2013-10-01", end="2014-01-31")

    requests = asyncio.run(collect_start_requests(spider))

    assert [request.url for request in requests] == [
        f"{BASE_URL}/diario-oficial-anos-anteriores/",
        f"{BASE_URL}/diario-oficial-2014/",
    ]


def test_parse_recent_editions_and_stop_pagination():
    spider = RnExtremozSpider(start="2026-09-29", end="2026-10-06")
    uploads = "https://extremoz.rn.gov.br/wp-content/uploads/2026"
    response = make_response(
        f"{BASE_URL}/diario-oficial-2026/",
        [
            make_item(
                "07 de Outubro de 2026",
                "07/10/2026",
                f"{uploads}/10/07-de-Outubro-de-2026.pdf",
            ),
            make_item(
                "06 de Outubro de 2026",
                "06/10/2026",
                f"{uploads}/10/06-de-Outubro-de-2026.pdf",
            ),
            make_item(
                "28 de Setembro de 2026 Edição Extra",
                "28/09/2026",
                f"{uploads}/09/28-de-Setembro-de-2026-Edicao-Extra.pdf",
            ),
        ],
        next_page_url=f"{BASE_URL}/diario-oficial-2026/page/2",
    )

    gazettes, requests = split_results(list(spider.parse(response)))

    assert len(gazettes) == 1
    assert gazettes[0]["date"] == date(2026, 10, 6)
    assert gazettes[0]["edition_number"] == ""
    assert gazettes[0]["is_extra_edition"] is False
    assert gazettes[0]["power"] == "executive_legislative"
    assert gazettes[0]["file_urls"] == [f"{uploads}/10/06-de-Outubro-de-2026.pdf"]
    assert requests == []


def test_parse_older_editions_use_date_from_title():
    spider = RnExtremozSpider(start="2011-01-01", end="2014-12-31")
    uploads = "https://extremoz.rn.gov.br/wp-content/uploads"
    response = make_response(
        f"{BASE_URL}/diario-oficial-2014/",
        [
            make_item(
                "Diário Oficial Do Município De Extremoz_29 DEZ 2014_EDIÇÃO ESPECIAL",
                "31/12/2014",
                f"{uploads}/2019/09/Extremoz_29-DEZ-2014_EDICAO-ESPECIAL.pdf",
            ),
            make_item(
                "Diário Oficial Do Município De Extremoz_19 DEZ 2014",
                "31/12/2014",
                None,
            ),
            make_item(
                "DOEM nº 0784, 22 de outubro de 2013",
                "05/10/2026",
                f"{uploads}/2019/09/Extremoz_22102013_Decrto-195_.pdf",
            ),
            make_item(
                "DOEM nº 0325, 1 de julho de 2011",
                "01/06/2024",
                f"{uploads}/2023/12/Edicao-NAO-ENCONTRADA.pdf",
            ),
        ],
        next_page_url=f"{BASE_URL}/diario-oficial-2014/page/2",
    )

    gazettes, requests = split_results(list(spider.parse(response)))

    assert [gazette["date"] for gazette in gazettes] == [
        date(2014, 12, 29),
        date(2013, 10, 22),
    ]
    assert gazettes[0]["is_extra_edition"] is True
    assert gazettes[1]["edition_number"] == "0784"
    assert gazettes[1]["is_extra_edition"] is False
    assert [request.url for request in requests] == [
        f"{BASE_URL}/diario-oficial-2014/page/2/"
    ]
