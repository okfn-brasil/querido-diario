import asyncio
from datetime import date

from scrapy.http import HtmlResponse

from gazette.spiders.mg.mg_montes_claros import MgMontesClarosSpider

LISTING_PDF_BASE = (
    "http://diariooficial.montesclaros.mg.gov.br/upload/diario-oficial/files/edicoes"
)


def make_response(url, body):
    return HtmlResponse(url=url, body=body.encode("utf-8"), encoding="utf-8")


async def collect_start_requests(spider):
    return [request async for request in spider.start()]


def test_start_requests_each_layout_for_its_period():
    spider = MgMontesClarosSpider(start="2015-12-20", end="2018-01-10")

    urls = [r.url for r in asyncio.run(collect_start_requests(spider))]

    assert urls[0] == f"{spider.BASE_URL}/2015/edicoes-de-2015"
    assert urls[1] == f"{spider.BASE_URL}/2016/janeiro"
    assert urls[-2] == f"{spider.BASE_URL}/2017/dezembro"
    assert urls[-1] == f"{spider.BASE_URL}/exercicio-2018"
    assert len(urls) == 1 + 24 + 1


def test_start_requests_only_months_inside_a_mid_year_range():
    spider = MgMontesClarosSpider(start="2016-03-15", end="2016-05-02")

    urls = [r.url for r in asyncio.run(collect_start_requests(spider))]

    assert urls == [
        f"{spider.BASE_URL}/2016/marco",
        f"{spider.BASE_URL}/2016/abril",
        f"{spider.BASE_URL}/2016/maio",
    ]


def test_parse_pdf_listing_reads_displayed_date_and_extra_edition():
    spider = MgMontesClarosSpider(start="2013-07-01", end="2014-12-31")
    body = f"""
        <a href="{LISTING_PDF_BASE}/2013/jul-13/Di%C3%A1rio%20Oficial%20Eletr%C3%B4nico%20Ano%201%20n%C2%BA%201-2013%20-%20010713.pdf">Diário Oficial Eletrônico – 02-07-13</a>
        <a href="{LISTING_PDF_BASE}/2014/mai-14/Di%C3%A1rio%20Oficial%20Eletr%C3%B4nico%20-%20Edi%C3%A7%C3%A3o%20Extra%20-16-05-14.pdf">Diário Oficial Eletrônico</a>
        <a href="{LISTING_PDF_BASE}/2015/dez-15/anexos%20lei%204841-15/01%20-%20Receita-Despesa.pdf">Anexo</a>
        <a href="{LISTING_PDF_BASE}/2016/jan-16/Di%C3%A1rio%20Oficial%20Eletr%C3%B4nico%2004-01-16.pdf">Diário Oficial Eletrônico -04-01-16</a>
    """
    response = make_response(f"{spider.BASE_URL}/2013/edicoes-de-2013", body)

    gazettes = list(spider.parse_pdf_listing(response))

    assert [(g["date"], g["is_extra_edition"]) for g in gazettes] == [
        (date(2013, 7, 2), False),
        (date(2014, 5, 16), True),
    ]


def test_parse_pdf_listing_moves_retired_host_links_to_upload_folder():
    spider = MgMontesClarosSpider(start="2014-02-01", end="2014-02-28")
    filename = "2014/fev-14/Di%C3%A1rio%20Oficial%20Eletr%C3%B4nico%2028-02-14.pdf"
    body = f"""
        <a href="http://montesclaros.mg.gov.br/diariooficial/{filename}">Diário Oficial Eletrônico – 28-02-14</a>
    """
    response = make_response(f"{spider.BASE_URL}/2014/edicoes-de-2014", body)

    (gazette,) = spider.parse_pdf_listing(response)

    assert gazette["file_urls"] == [f"{spider.UPLOAD_URL}{filename}"]


def test_parse_editions_follows_dated_links_in_range():
    spider = MgMontesClarosSpider(start="2022-12-30", end="2022-12-31")
    body = """
        <a href="/2022/dezembro/diario-oficial-eletronico-30122022-edicao-extra">Diário Oficial Eletrônico 30/12/2022 - Edição Extra</a>
        <a href="/2022/dezembro/diario-oficial-eletronico-29122022">Diário Oficial Eletrônico 29/12/2022</a>
        <a href="/2023/janeiro/lista-unica-publicada-no-diario-oficial-eletronico-de-21">Lista</a>
    """
    response = make_response(f"{spider.BASE_URL}/exercicio-2022", body)

    requests = list(spider.parse_editions(response))

    assert len(requests) == 1
    assert requests[0].cb_kwargs == {
        "gazette_date": date(2022, 12, 30),
        "is_extra_edition": True,
    }


def test_parse_editions_takes_year_from_path_when_slug_is_truncated():
    spider = MgMontesClarosSpider(start="2022-10-01", end="2022-10-31")
    body = """
        <a href="/2022/outubro/diario-oficial-eletronico-0510202">Diário Oficial Eletrônico 05/10/202</a>
    """
    response = make_response(f"{spider.BASE_URL}/exercicio-2022", body)

    (request,) = spider.parse_editions(response)

    assert request.cb_kwargs["gazette_date"] == date(2022, 10, 5)


def test_parse_gazette_page_extracts_pdf_from_redirect_script():
    spider = MgMontesClarosSpider()
    pdf_url = "https://admin.montesclaros.mg.gov.br/upload/diario-oficial/files/edicoes/2025/dez-25/DiarioOficialEletronico31-12-25.pdf"
    body = (
        f"<script>window.onload = function(){{window.location = '{pdf_url}'}};</script>"
    )
    response = make_response(f"{spider.BASE_URL}/2025/dezembro/x", body)

    (gazette,) = spider.parse_gazette_page(response, date(2025, 12, 31), False)

    assert gazette["file_urls"] == [pdf_url]


def test_parse_gazette_page_skips_page_without_pdf():
    spider = MgMontesClarosSpider()
    body = "<script>if (window.location.hostname === 'x') {}</script>"
    response = make_response(f"{spider.BASE_URL}/2018/janeiro/x", body)

    assert list(spider.parse_gazette_page(response, date(2018, 1, 20), False)) == []


def test_parse_date_skips_invalid_dates():
    spider = MgMontesClarosSpider()

    assert spider._parse_date("31/02/2019") is None
    assert spider._parse_date("05/10/202") is None
    assert spider._parse_date("Edição de 2015") is None
