from datetime import date

from scrapy.http import HtmlResponse

from gazette.spiders.rn.rn_macaiba import RnMacaibaSpider

LISTING_URL = "https://macaiba.rn.gov.br/servicos/diario-oficial/"
NEXT_PAGE_URL = f"{LISTING_URL}page/2/"


def make_response(*gazettes):
    items = "".join(
        f"""
        <li class="link_item">
            <a href="{href}" target="_blank">{title}
                <span>visualizar</span>
            </a>
        </li>
        """
        for title, href in gazettes
    )
    body = f"""
    <ul>{items}</ul>
    <a class="nextpostslink" rel="next" href="{NEXT_PAGE_URL}">»</a>
    """
    return HtmlResponse(url=LISTING_URL, body=body.encode("utf-8"), encoding="utf-8")


def parse(spider, response):
    results = list(spider.parse(response))
    gazettes = [result for result in results if not hasattr(result, "url")]
    requests = [result for result in results if hasattr(result, "url")]
    return gazettes, requests


def test_parse_gazettes_and_follow_next_page():
    spider = RnMacaibaSpider(start="2026-09-01", end="2026-10-07")
    response = make_response(
        (
            "DOMM 2043 - 06/outubro/2026",
            "https://macaiba.rn.gov.br/wp-content/uploads/2026/10/DOMM-2043.pdf",
        ),
        (
            "DOMM 0812 – Edição Extraordinária - 30/setembro/2026",
            "https://macaiba.rn.gov.br/wp-content/uploads/2026/09/DOMM-812.pdf",
        ),
    )

    gazettes, requests = parse(spider, response)

    assert [
        (gazette["date"], gazette["edition_number"], gazette["is_extra_edition"])
        for gazette in gazettes
    ] == [
        (date(2026, 10, 6), "2043", False),
        (date(2026, 9, 30), "812", True),
    ]
    assert gazettes[0]["file_urls"] == [
        "https://macaiba.rn.gov.br/wp-content/uploads/2026/10/DOMM-2043.pdf"
    ]
    assert gazettes[0]["power"] == "executive_legislative"
    assert [request.url for request in requests] == [NEXT_PAGE_URL]


def test_parse_follows_next_page_when_oldest_gazette_is_on_start_date():
    spider = RnMacaibaSpider(start="2026-09-30", end="2026-10-07")
    response = make_response(
        (
            "DOMM 2039 - 30/setembro/2026",
            "https://macaiba.rn.gov.br/wp-content/uploads/2026/09/DOMM-2039.pdf",
        ),
    )

    _, requests = parse(spider, response)

    assert [request.url for request in requests] == [NEXT_PAGE_URL]


def test_parse_stops_pagination_before_start_date():
    spider = RnMacaibaSpider(start="2026-09-30", end="2026-10-07")
    response = make_response(
        (
            "DOMM 2039 - 30/setembro/2026",
            "https://macaiba.rn.gov.br/wp-content/uploads/2026/09/DOMM-2039.pdf",
        ),
        (
            "DOMM 2038 - 29/setembro/2026",
            "https://macaiba.rn.gov.br/wp-content/uploads/2026/09/DOMM-2038.pdf",
        ),
    )

    gazettes, requests = parse(spider, response)

    assert [gazette["edition_number"] for gazette in gazettes] == ["2039"]
    assert requests == []


def test_parse_fixes_year_from_old_website_file_path():
    spider = RnMacaibaSpider(start="2018-12-01", end="2018-12-31")
    response = make_response(
        (
            "DOMM 0143 - 19/dezembro/2019",
            "https://antigo.macaiba.rn.gov.br/_ups/boletins/2018/12/19/e624f14b.pdf",
        ),
        (
            "BOMM 1282 - 30/junho/2017",
            "https://antigo.macaiba.rn.gov.br/_ups/boletins/2017/08/14/bb203c7c.pdf",
        ),
    )

    gazettes, _ = parse(spider, response)

    assert [(gazette["date"], gazette["edition_number"]) for gazette in gazettes] == [
        (date(2018, 12, 19), "143")
    ]
