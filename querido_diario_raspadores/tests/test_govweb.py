import asyncio
from datetime import date

from scrapy.http import HtmlResponse, Request

from gazette.spiders.base.govweb import BaseGovWebSpider


class GovWebSpiderForTest(BaseGovWebSpider):
    TERRITORY_ID = "0000000"
    name = "govweb_test"
    base_url = "https://www.example.to.gov.br"
    start_date = date(2026, 1, 1)


def make_spider():
    return GovWebSpiderForTest(start="2026-09-01", end="2026-09-30")


async def collect_start_requests(spider):
    return [request async for request in spider.start()]


def edition_card(number, raw_date, edition_id, badge=""):
    badge_html = f'<span class="badge"><i></i> {badge} </span>' if badge else ""
    return f"""
    <div class="card">
        <div class="header">
            <div>
                <h3>Edição Nº {number}</h3>
                <p>{raw_date}</p>
            </div>
            <div class="badges">{badge_html}</div>
        </div>
        <div class="actions">
            <a href="https://www.example.to.gov.br/diariooficial/materias/{edition_id}">Matérias</a>
            <a href="https://www.example.to.gov.br/diariooficial/view/{edition_id}">Visualizar</a>
        </div>
    </div>
    """


def make_response(cards, last_page=None, page=1):
    search_url = (
        "https://www.example.to.gov.br/diariooficial/pesquisa/all/all/"
        "2026-09-01/2026-09-30"
    )
    paginator = ""
    if last_page:
        links = "".join(
            f'<a class="paginator_item" href="{search_url}/{p}">{p}</a>'
            for p in range(1, last_page + 1)
        )
        paginator = f'<nav class="paginator">{links}</nav>'
    body = f"<html><body><div>{''.join(cards)}</div>{paginator}</body></html>"
    return HtmlResponse(
        url=f"{search_url}/{page}", body=body.encode("utf-8"), encoding="utf-8"
    )


def test_start_builds_date_filtered_search_request():
    spider = make_spider()

    start_requests = asyncio.run(collect_start_requests(spider))

    assert len(start_requests) == 1
    assert start_requests[0].url == (
        "https://www.example.to.gov.br/diariooficial/pesquisa/all/all/"
        "2026-09-01/2026-09-30/1"
    )
    assert spider.allowed_domains == ["www.example.to.gov.br"]


def test_parse_yields_regular_and_supplementary_editions():
    spider = make_spider()
    response = make_response(
        [
            edition_card(
                748, "terça, 29 de setembro de 2026", "74820261135", "Suplementar"
            ),
            edition_card(748, "terça, 29 de setembro de 2026", "74820261133"),
        ]
    )

    gazettes = list(spider.parse(response, page=2))

    assert [(g["edition_number"], g["is_extra_edition"]) for g in gazettes] == [
        ("748", True),
        ("748", False),
    ]
    assert gazettes[0]["date"] == date(2026, 9, 29)
    assert gazettes[0]["file_urls"] == [
        "https://www.example.to.gov.br/download/diariooficial/edition/74820261135"
    ]
    assert gazettes[0]["power"] == "executive"


def test_parse_skips_editions_outside_the_date_range():
    # a plataforma tem edições com datas cadastradas de forma errada (ex.: 2006)
    spider = make_spider()
    response = make_response(
        [
            edition_card(159, "quinta, 14 de dezembro de 2006", "1592006"),
            edition_card(740, "quarta, 16 de setembro de 2026", "74020261124"),
        ]
    )

    gazettes = list(spider.parse(response, page=2))

    assert [g["edition_number"] for g in gazettes] == ["740"]


def test_parse_requests_remaining_pages_only_from_the_first_page():
    spider = make_spider()
    cards = [edition_card(740, "quarta, 16 de setembro de 2026", "74020261124")]

    first_page_results = list(spider.parse(make_response(cards, last_page=3), page=1))
    other_page_results = list(
        spider.parse(make_response(cards, last_page=3, page=2), page=2)
    )

    requests = [r for r in first_page_results if isinstance(r, Request)]
    assert [r.url[-1] for r in requests] == ["2", "3"]
    assert [r.cb_kwargs for r in requests] == [{"page": 2}, {"page": 3}]
    assert not any(isinstance(r, Request) for r in other_page_results)
