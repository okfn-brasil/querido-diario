import asyncio
from datetime import date
from urllib.parse import parse_qs, urlparse

from scrapy.http import HtmlResponse

from gazette.spiders.rj.rj_sao_goncalo import RjSaoGoncaloSpider

HIGHLIGHT = '<spam class="badge bg-warning text-dark">A</spam>'


async def collect_start_requests(spider):
    return [request async for request in spider.start()]


def card(href, raw_date, body, extra=False):
    extra_label = (
        "<font color='red' size='3'>Diário Oficial Extraordinário</font> - "
        if extra
        else "&nbsp"
    )
    return f"""
    <div class="card mb-3">
        <div class="card-header">
            <b>
                {extra_label} 443 Palavra(s) <font color="red">a</font>
                encontrada(s) no Diário Oficial em
                <a href="{href}" underline="none" target="_blank">{raw_date}</a>.
            </b>
        </div>
        <div class="card-body"><p>{body}</p></div>
    </div>
    """


def pagination(current, last):
    links = "".join(
        f"<a href=index?NumeroPagina={n}&Termo=a&PesquisarTermo=Pesquisar>"
        f"<font color='#030f3d' size='2'>{n}</font></a>&nbsp;&nbsp;"
        for n in range(1, last + 1)
        if n != current
    )
    return f"""
    <div class="d-flex justify-content-center mt-1">
        <ul class="pagination pagination-sm">
        <font color='red' face='arial' size='4'><b>{current}</b></font>{links}
    </div>
    """


def make_response(cards, current_page=1, last_page=1):
    html = f"""
    <html><body><main>
    <div class="container mt-1">{"".join(cards)}{pagination(current_page, last_page)}</div>
    </main></body></html>
    """
    return HtmlResponse(
        url=f"https://do.pmsg.rj.gov.br/index?NumeroPagina={current_page}",
        body=html.encode("utf-8"),
        encoding="utf-8",
    )


def test_start_searches_the_whole_requested_period():
    spider = RjSaoGoncaloSpider(start="2026-09-01", end="2026-09-20")

    start_requests = asyncio.run(collect_start_requests(spider))

    assert len(start_requests) == 1
    query = parse_qs(urlparse(start_requests[0].url).query)
    assert query["NumeroPagina"] == ["1"]
    assert query["DataInicial"] == ["2026-09-01"]
    assert query["DataFinal"] == ["2026-09-20"]
    assert query["Termo"] == ["a"]


def test_parse_reads_edition_number_in_both_header_formats():
    spider = RjSaoGoncaloSpider()
    response = make_response(
        [
            card(
                "diario/2026_09_18.pdf",
                "18/09/2026",
                f"DIÁRIO OFICI{HIGHLIGHT}L PODER EXECUTIVO | 18 DE SETEMBRO | EDIÇÃO N°1.771",
            ),
            card(
                "diario/2024_08_21.pdf",
                "21/08/2024",
                "D.O.E. | PODER EXECUTIVO | ANO V | N.º 1.196 EM 21 DE AGOSTO DE",
            ),
        ]
    )

    gazettes = list(spider.parse(response, page=1))

    assert [g["edition_number"] for g in gazettes] == ["1771", "1196"]
    assert gazettes[0]["date"] == date(2026, 9, 18)
    assert gazettes[0]["file_urls"] == [
        "https://do.pmsg.rj.gov.br/diario/2026_09_18.pdf"
    ]
    assert gazettes[0]["power"] == "executive"


def test_parse_reads_edition_number_with_space_after_thousands_dot():
    spider = RjSaoGoncaloSpider()
    response = make_response(
        [
            card(
                "diario/2025_03_10.pdf",
                "10/03/2025",
                "10 DE MARÇO DE 2025 | EDIÇÃO N°1. 362 PREFEITURA",
            ),
        ]
    )

    [gazette] = spider.parse(response, page=1)

    assert gazette["edition_number"] == "1362"


def test_parse_flags_extraordinary_editions():
    spider = RjSaoGoncaloSpider()
    response = make_response(
        [
            card(
                "diario/2024_08_21_1.pdf",
                "21/08/2024",
                "D.O.E. | PODER EXECUTIVO | ANO V | N.º 1.197 EM 21 DE AGOSTO DE",
                extra=True,
            ),
        ]
    )

    [gazette] = spider.parse(response, page=1)

    assert gazette["is_extra_edition"] is True
    assert gazette["edition_number"] == "1197"
    assert gazette["file_urls"] == ["https://do.pmsg.rj.gov.br/diario/2024_08_21_1.pdf"]


def test_parse_ignores_numbers_before_editions_were_numbered():
    spider = RjSaoGoncaloSpider()
    response = make_response(
        [card("diario/2019_05_10.pdf", "10/05/2019", "DECRETO Nº 123/2019")]
    )

    [gazette] = spider.parse(response, page=1)

    assert gazette["edition_number"] == ""
    assert gazette["is_extra_edition"] is False


def test_parse_fixes_links_with_two_digit_year():
    spider = RjSaoGoncaloSpider()
    response = make_response([card("diario/17_01_21.pdf", "21/01/2017", "")])

    [gazette] = spider.parse(response, page=1)

    assert gazette["file_urls"] == ["https://do.pmsg.rj.gov.br/diario/2017_01_21.pdf"]


def test_parse_skips_an_edition_already_listed():
    spider = RjSaoGoncaloSpider()
    same_card = card("diario/2020_04_20.pdf", "20/04/2020", "")

    first_page = list(spider.parse(make_response([same_card]), page=1))
    second_page = list(spider.parse(make_response([same_card]), page=2))

    assert len(first_page) == 1
    assert second_page == []


def test_parse_follows_to_the_next_page_until_the_last():
    spider = RjSaoGoncaloSpider()

    middle = list(spider.parse(make_response([], current_page=2, last_page=3), page=2))
    last = list(spider.parse(make_response([], current_page=3, last_page=3), page=3))

    assert len(middle) == 1
    assert parse_qs(urlparse(middle[0].url).query)["NumeroPagina"] == ["3"]
    assert middle[0].cb_kwargs == {"page": 3}
    assert last == []
