from datetime import date
from urllib.parse import parse_qs

import pytest
from scrapy import Request, signals
from scrapy.exceptions import StopDownload
from scrapy.http import HtmlResponse, Response
from scrapy.utils.test import get_crawler
from twisted.python.failure import Failure

from gazette.spiders.sp.sp_sao_paulo import SpSaoPauloSpider

# Public HTML fragments from fixtures-sp, captured on 2026-11-26.
LISTING = (
    '<form id="frmEpubliMemoria" method="post"><input type="hidden" id'
    '="hdnFiltroMandato" name="hdnFiltroMandato" value=""><input type='
    '"hidden" id="hdnFiltroAno" name="hdnFiltroAno" value=""><input ty'
    'pe="hidden" id="hdnFiltroMes" name="hdnFiltroMes" value=""><input'
    ' type="hidden" id="hdnInicio" name="hdnInicio" value="0"><input t'
    'ype="hidden" id="hdnAcao" value="memoria_listar"></form><div clas'
    's="mandato-ano" data-value="54,2026">2026</div><div class="mandat'
    'o-ano" data-value="54,2025">2025</div><div class="mandato-ano" da'
    'ta-value="54,2024">2024</div>'
)
EDITIONS = (
    '<div class="painelEdições clearfix"><a href="http://diariooficial'
    ".prefeitura.sp.gov.br/md_epubli_memoria_arquivo.php?VRR8ZWUNFStCS"
    "UYQdxSxF_qMvUN2gixAVyU4R1LcXbCbTxR93_UEEdMD9LcHcc4WwasbPCVHvZzfic"
    'q71D_Xww,," target="_blank" class="boxCapaEdicao comImagem" title'
    '="03/11/2026">\n                                <img src="http://d'
    "iariooficial.prefeitura.sp.gov.br/md_epubli_memoria_arquivo.php?j"
    "_v3GK9_qIBrus7HA38jXFTBo5gsqoLCFQ0iX1nOP9OIuBqwqgDhmIw8vZFrt9g2-Z"
    'z8Of7f7F76vS6jjsJzbw,," class="img-responsive" alt="Imagem ilustr'
    'ativa">\n                                <span class="campoLegenda'
    '">\n                                    <span class="legenda">\n   '
    "                                     <h3>03/11</h3><hr><h3>2026</"
    "h3>\n                                    </span>\n                 "
    '                   <span class="sombra"></span>\n                 '
    "               </span>\n                               </a><a href"
    '="http://diariooficial.prefeitura.sp.gov.br/md_epubli_memoria_arq'
    "uivo.php?2cmhJY2Fo_IW0RcdSK9nfz1O8kVve7uEWP3Jy1pxZFx6xYITWrvAqXIQ"
    'Mu7Y2zADa_Ib6GBD-9rJ_cc3uaojOQ,," target="_blank" class="boxCapaE'
    'dicao comImagem" title="04/11/2026">\n                            '
    '    <img src="http://diariooficial.prefeitura.sp.gov.br/md_epubli'
    "_memoria_arquivo.php?fRw0F8seF_vjXmZuLyIWhDQ1LKEfKZ5khx5SnghXexHf"
    'FY5HfUVMMTIjlGJ5jV_I8jiKq4kQqi5MSPy8LZ4mmw,," class="img-responsi'
    've" alt="Imagem ilustrativa">\n                                <sp'
    'an class="campoLegenda">\n                                    <spa'
    'n class="legenda">\n                                        <h3>04'
    "/11</h3><hr><h3>2026</h3>\n                                    </s"
    'pan>\n                                    <span class="sombra"></s'
    "pan>\n                                </span>\n                    "
    '           </a><a href="http://diariooficial.prefeitura.sp.gov.br'
    "/md_epubli_memoria_arquivo.php?rK9LepJR43kog4rqfNNGgT5tBz6xSXzvSs"
    'WNIYhR9OvVr9znoGgAikUwPU1CU4bYZ343X-toTm1rlhsY6ipIEQ,," target="_'
    'blank" class="boxCapaEdicao comImagem" title="05/11/2026">\n      '
    '                          <img src="http://diariooficial.prefeitu'
    "ra.sp.gov.br/md_epubli_memoria_arquivo.php?jTFY-G_H0xeYjzG-w6bB1y"
    "9ee1cRWfi2eHMsQsgb9DP3rV19wtkwbb4W4bzFk9ERnhwTadRkBJg566b2AHYpPg,"
    '," class="img-responsive" alt="Imagem ilustrativa">\n             '
    '                   <span class="campoLegenda">\n                  '
    '                  <span class="legenda">\n                        '
    "                <h3>05/11</h3><hr><h3>2026</h3>\n                 "
    "                   </span>\n                                    <s"
    'pan class="sombra"></span>\n                                </span'
    ">\n                               </a></div>"
)


def html(body):
    return HtmlResponse(
        url=SpSaoPauloSpider.start_urls[0],
        body=body.encode(),
        encoding="utf-8",
    )


@pytest.mark.parametrize(
    "start,end,expected",
    [
        ("2026-11-03", "2026-11-05", [(2026, 11)]),
        ("2025-12-31", "2026-02-01", [(2026, 1), (2026, 2), (2025, 12)]),
        ("2026-01-31", "2026-03-01", [(2026, 1), (2026, 2), (2026, 3)]),
        ("2026-11-05", "2026-11-03", []),
    ],
)
def test_month_requests(start, end, expected):
    spider = SpSaoPauloSpider(start=start, end=end)
    requests = list(spider.parse(html(LISTING)))
    actual = []
    for request in requests:
        fields = parse_qs(request.body.decode())
        year = int(fields["hdnFiltroAno"][0])
        month = int(fields["hdnFiltroMes"][0])
        actual.append((year, month))
        assert fields["hdnFiltroMandato"] == [f"54,{year}"]
        assert fields["hdnInicio"] == ["0"]
        assert request.method == "POST"
        assert request.callback == spider.parse_editions
    assert actual == expected


def test_defaults():
    spider = SpSaoPauloSpider()
    assert spider.start_date == date(2017, 6, 1)
    assert spider.zyte_smartproxy_enabled is False


def test_editions_require_pdf_before_emitting_gazette():
    spider = SpSaoPauloSpider(start="2026-11-03", end="2026-11-04")
    requests = list(spider.parse_editions(html(EDITIONS)))
    assert len(requests) == 2
    for request, day in zip(requests, (3, 4)):
        assert request.url.startswith("https://")
        response = Response(request.url, body=b"%PDF-1.4\nreal gazette")
        items = list(request.callback(response, **request.cb_kwargs))
        assert len(items) == 1
        assert items[0]["date"] == date(2026, 11, day)
        assert items[0]["file_urls"] == [request.url]
        assert items[0]["power"] == "executive"
        assert items[0]["is_extra_edition"] is False


@pytest.mark.parametrize(
    "body",
    [
        b'<html><script>window["bobcmn"] = 1;</script></html>',
        b"<html>TSPD challenge</html>",
        b"<html>cf-turnstile</html>",
        b"<html>server error</html>",
        b"",
    ],
)
def test_invalid_download_never_emits_gazette(body, caplog):
    spider = SpSaoPauloSpider(start="2026-11-03", end="2026-11-05")
    request = next(spider.parse_editions(html(EDITIONS)))
    response = Response(
        request.url, body=body, headers={"Content-Type": "application/pdf"}
    )
    assert list(request.callback(response, **request.cb_kwargs)) == []
    assert "challenge" in caplog.text or "expected PDF" in caplog.text


def test_failed_status_never_emits_gazette(caplog):
    spider = SpSaoPauloSpider()
    response = Response("https://example.org/edition", status=503, body=b"%PDF-1.4")
    assert list(spider.parse_pdf(response, date(2026, 11, 3))) == []
    assert "expected PDF" in caplog.text


@pytest.mark.parametrize("prefix,expected", [(b"%PDF-1.4\n", 1), (b"<html>TSPD", 0)])
def test_partial_download_through_signals(prefix, expected):
    crawler = get_crawler(SpSaoPauloSpider)
    spider = SpSaoPauloSpider.from_crawler(
        crawler, start="2026-11-03", end="2026-11-03"
    )
    request = next(spider.parse_editions(html(EDITIONS)))
    assert request.meta["check_pdf"] is True
    # Simulate a retry: headers must reset the previous response's count.
    request.meta["pdf_bytes_received"] = 8000
    crawler.signals.send_catch_log(
        signals.headers_received,
        headers={},
        body_length=11000000,
        request=request,
        spider=spider,
    )
    body = prefix.ljust(8192, b" ")
    for chunk in (body[:4096], body[4096:]):
        results = crawler.signals.send_catch_log(
            signals.bytes_received, data=chunk, request=request, spider=spider
        )
        failures = [r for _, r in results if isinstance(r, Failure)]
        if request.meta["pdf_bytes_received"] < 8192:
            assert failures == []
        else:
            assert len(failures) == 1
            assert isinstance(failures[0].value, StopDownload)
            assert failures[0].value.fail is False
    response = Response(
        request.url, body=body, request=request, flags=["download_stopped"]
    )
    items = list(request.callback(response, **request.cb_kwargs))
    assert len(items) == expected
    if items:
        assert items[0]["date"] == date(2026, 11, 3)
        assert items[0]["file_urls"] == [request.url]
    # The pipeline's separate request must be allowed to download the full PDF.
    for other in (Request(request.url), Request(spider.start_urls[0])):
        results = crawler.signals.send_catch_log(
            signals.bytes_received,
            data=b"x" * 16384,
            request=other,
            spider=spider,
        )
        assert all(not isinstance(r, Failure) for _, r in results)
        assert "pdf_bytes_received" not in other.meta
