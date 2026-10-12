from datetime import date

import pytest
from scrapy.http import HtmlResponse, Response

from gazette.items import Gazette
from gazette.spiders.base.instar import BaseInstarSpider

VIEWER_URL = "https://web.santoandre.sp.gov.br/portal/diario-oficial/ver/252/"
PDF_URL = (
    "https://web.santoandre.sp.gov.br/uploads/d4501703f900bf2126513523ff73156f.pdf"
)

# Página reduzida do visualizador PDF.js (`/diario-oficial/ver/<id>/`).
VIEWER_HTML = """
<html><head><title>Diário Oficial /2021</title></head>
<body>
<div class="d_titulo_acessibildiade">Acessibilidade</div>
<script>
const defaultOptions = {
  cursorToolOnLoad: {
    value: 0,
    kind: OptionKind.VIEWER + OptionKind.PREFERENCE
  },
  defaultUrl: {
    value: '/uploads/d4501703f900bf2126513523ff73156f.pdf',
    kind: OptionKind.VIEWER
  },
  defaultZoomValue: {
    value: "",
    kind: OptionKind.VIEWER + OptionKind.PREFERENCE
  }
};
</script>
</body></html>
"""


class InstarSpiderForTest(BaseInstarSpider):
    TERRITORY_ID = "0000000"
    name = "instar_test"
    base_url = "https://web.santoandre.sp.gov.br/portal/diario-oficial"
    start_date = date(2021, 10, 28)


@pytest.fixture
def spider():
    return InstarSpiderForTest(start="2021-10-28", end="2021-10-28")


@pytest.fixture
def item():
    return Gazette(
        date=date(2021, 10, 28),
        edition_number="2644",
        is_extra_edition=False,
        power="executive_legislative",
    )


def html_response(body, url=VIEWER_URL):
    return HtmlResponse(url=url, body=body.encode("utf-8"), encoding="utf-8")


def test_viewer_page_yields_pdf_url_instead_of_page_url(spider, item):
    results = list(spider.parse_gazette_url(html_response(VIEWER_HTML), item))

    assert len(results) == 1
    assert results[0]["file_urls"] == [PDF_URL]
    assert results[0]["date"] == date(2021, 10, 28)
    assert results[0]["edition_number"] == "2644"


def test_explicit_download_link_has_priority(spider, item):
    html = VIEWER_HTML.replace(
        "<body>",
        '<body><div class="d_titulo_edicao"><a href="/uploads/direto.pdf">Baixar</a></div>',
    )

    results = list(spider.parse_gazette_url(html_response(html), item))

    assert results[0]["file_urls"] == [
        "https://web.santoandre.sp.gov.br/uploads/direto.pdf"
    ]


def test_double_quoted_default_url(spider, item):
    html = VIEWER_HTML.replace("'/uploads/", '"/uploads/').replace(".pdf'", '.pdf"')

    results = list(spider.parse_gazette_url(html_response(html), item))

    assert results[0]["file_urls"] == [PDF_URL]


def test_empty_default_url_does_not_yield_the_viewer_page(spider, item, caplog):
    html = VIEWER_HTML.replace("'/uploads/d4501703f900bf2126513523ff73156f.pdf'", '""')

    results = list(spider.parse_gazette_url(html_response(html), item))

    assert results == []
    assert "Nenhum arquivo encontrado" in caplog.text


def test_page_without_viewer_options_does_not_yield_the_page_url(spider, item):
    results = list(
        spider.parse_gazette_url(html_response("<html><body></body></html>"), item)
    )

    assert results == []


def test_image_attachment_is_kept(spider, item):
    html = VIEWER_HTML.replace(
        "d4501703f900bf2126513523ff73156f.pdf", "ec6fc9024893e732c971139514315595.jpg"
    )

    results = list(spider.parse_gazette_url(html_response(html), item))

    assert results[0]["file_urls"] == [
        "https://web.santoandre.sp.gov.br/uploads/ec6fc9024893e732c971139514315595.jpg"
    ]


def test_response_that_is_already_the_file_is_used_as_is(spider, item):
    response = Response(url=PDF_URL, body=b"%PDF-1.4 ...")

    results = list(spider.parse_gazette_url(response, item))

    assert results[0]["file_urls"] == [PDF_URL]
