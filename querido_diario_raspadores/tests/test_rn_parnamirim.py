import asyncio
import json
from datetime import date

from scrapy.http import HtmlResponse, TextResponse

from gazette.spiders.rn.rn_parnamirim import RnParnamirimSpider


async def collect_start_requests(spider):
    return [request async for request in spider.start()]


def make_old_website_response(*gazettes):
    items = "".join(
        f"""
        <li>
            <span class="texto">{raw_date} - </span>
            <a class="linkDarkenedStyle" href="{href}" target="_blank">{title}</a> -
            <a class="linkDarkenedStyle" href="{href}" download>download</a>
        </li>
        """
        for raw_date, title, href in gazettes
    )
    body = f'<div class="sub-dropdown"><ul><ul>{items}</ul></ul></div>'
    return HtmlResponse(
        url=RnParnamirimSpider.OLD_WEBSITE_URL,
        body=body.encode("utf-8"),
        encoding="utf-8",
    )


def make_api_response(payload):
    return TextResponse(
        url=f"{RnParnamirimSpider.SGIDOM_API_URL}?data=2019-03",
        body=json.dumps(payload).encode("utf-8"),
        encoding="utf-8",
    )


def test_start_requests_only_sgidom_months_after_transition():
    spider = RnParnamirimSpider(start="2026-09-20", end="2026-10-07")

    start_requests = asyncio.run(collect_start_requests(spider))

    assert [request.url for request in start_requests] == [
        f"{RnParnamirimSpider.SGIDOM_API_URL}?data=2026-09",
        f"{RnParnamirimSpider.SGIDOM_API_URL}?data=2026-10",
    ]


def test_start_requests_old_website_and_sgidom_around_transition():
    spider = RnParnamirimSpider(start="2018-07-01", end="2018-08-05")

    start_requests = asyncio.run(collect_start_requests(spider))

    assert [request.url for request in start_requests] == [
        RnParnamirimSpider.OLD_WEBSITE_URL,
        f"{RnParnamirimSpider.SGIDOM_API_URL}?data=2018-07",
        f"{RnParnamirimSpider.SGIDOM_API_URL}?data=2018-08",
    ]


def test_parse_old_website_skips_gazettes_published_in_sgidom():
    spider = RnParnamirimSpider(start="2018-07-01", end="2018-08-05")
    response = make_old_website_response(
        ("17 de Julho de 2018", "DOM nº 2565 Dia 17", "pdf/diario/DOM2565.pdf"),
        (
            "11 de Julho de 2018",
            "DOM nº 2560 - Edição Especial Dia 11",
            "pdf/diario/DOM%202560.pdf",
        ),
        ("29 de Junho de 2018", "DOM nª 2551 Dia 29", "pdf/diario/DOM2551.pdf"),
    )

    gazettes = list(spider.parse_old_website(response))

    assert len(gazettes) == 1
    assert gazettes[0]["date"] == date(2018, 7, 11)
    assert gazettes[0]["edition_number"] == "2560"
    assert gazettes[0]["is_extra_edition"] is True
    assert gazettes[0]["file_urls"] == [
        "https://antigo.parnamirim.rn.gov.br/pdf/diario/DOM%202560.pdf"
    ]


def test_parse_old_website_edition_number_formats():
    spider = RnParnamirimSpider(start="2009-01-01", end="2018-07-16")
    response = make_old_website_response(
        ("19 de Abril de 2018", "DOM n• 2506 Dia 19", "pdf/diario/a.pdf"),
        ("02 de Outubro de 2017", "DOM 2415 n° Dia 02", "pdf/diario/b.pdf"),
        ("10 de Março de 2011", "DOM1137 - Dia 10", "pdf/diario/c.pdf"),
        ("30 de Abril de 2010", "DOM nº 0331 - Dia 30 - ESPECIAL", "pdf/diario/d.pdf"),
        ("13 de Janeiro de 2009", " BO - Nº 54 - Dia 13", "pdf/diario/e.pdf"),
        ("05 de Maio de 2015", "DOM Edição Especial", "pdf/diario/f.pdf"),
    )

    gazettes = list(spider.parse_old_website(response))

    assert [gazette["edition_number"] for gazette in gazettes] == [
        "2506",
        "2415",
        "1137",
        "331",
        "54",
        "",
    ]
    assert [gazette["is_extra_edition"] for gazette in gazettes] == [
        False,
        False,
        False,
        True,
        False,
        True,
    ]


def test_parse_sgidom_builds_pdf_export_request():
    spider = RnParnamirimSpider(start="2019-03-01", end="2019-03-31")
    response = make_api_response(
        [
            {
                "id": 206,
                "numero": "DOM2741 - Edição Especial",
                "status": True,
                # 2019-03-30 00:00 em Brasília
                "data_publicacao": 1553914800000,
            },
            {
                "id": 180,
                "numero": "DOM2721",
                "status": True,
                # 2019-02-28 00:00 em Brasília, fora do intervalo
                "data_publicacao": 1551322800000,
            },
        ]
    )

    gazettes = list(spider.parse(response))

    assert len(gazettes) == 1
    assert gazettes[0]["date"] == date(2019, 3, 30)
    assert gazettes[0]["edition_number"] == "2741"
    assert gazettes[0]["is_extra_edition"] is True

    file_request = gazettes[0]["file_requests"][0]
    assert file_request.method == "POST"
    assert file_request.url == (
        "https://sgidomhtmltopdf.parnamirim.rn.gov.br/export?id_diario=206"
    )
    assert json.loads(file_request.body) == {
        "domQueryParams": "publicar=false&id_diario=206&",
        "domDataCabecalho": "30/03/2019",
        "domOrigin": "https://diariooficial.parnamirim.rn.gov.br",
        "diarioId": 206,
    }
