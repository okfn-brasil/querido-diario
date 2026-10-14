from datetime import date

from scrapy.http import HtmlResponse, Request

from gazette.spiders.se.se_aracaju import SeAracajuSpider

LISTING_URL = "https://sga.aracaju.se.gov.br/legislacao/faces/diario_form_pesq.jsp"
LAST_BODY = (
    "javax.faces.ViewState=j_id2&AJAXREQUEST=j_id_0"
    "&formPesquisarDiario%3Aj_id_23=3&formPesquisarDiario%3Aj_id_26=2026"
)


def cell(raw_date, number, labels=()):
    downloads = "".join(
        f'<table><tbody><tr><td><span class="label">{label}</span></td></tr>'
        "</tbody></table>"
        for label in labels
    )
    return (
        '<td class="rich-table-cell"><div class="rich-panel">'
        f'<div class="rich-panel-header">{raw_date}</div>'
        '<div class="rich-panel-body pbody"><table><tbody>'
        '<tr><td><span class="label">Número:</span></td></tr>'
        f"<tr><td>{number}</td></tr></tbody></table>{downloads}</div></div></td>"
    )


def make_response(cells, pager=""):
    body = (
        '<html xmlns="http://www.w3.org/1999/xhtml"><body><table><tbody>'
        f'<tr class="rich-table-row">{"".join(cells)}</tr></tbody></table>'
        f"{pager}</body></html>"
    )
    request = Request(LISTING_URL, method="POST", body=LAST_BODY)
    return HtmlResponse(
        LISTING_URL, body=body.encode("utf-8"), encoding="utf-8", request=request
    )


def make_spider():
    return SeAracajuSpider(start_date=date(2026, 3, 1), end_date=date(2026, 3, 31))


def test_edition_without_download_label_is_collected():
    response = make_response([cell("31/03/2026", "5828")])

    items = list(make_spider().parse_page_result(response))

    assert len(items) == 1
    assert items[0]["date"] == date(2026, 3, 31)
    assert items[0]["edition_number"] == "5828"
    assert items[0]["is_extra_edition"] is False
    assert items[0]["file_urls"] == ["https://sga.aracaju.se.gov.br/diarios/5828.pdf"]


def test_regular_and_supplementary_labels_yield_two_editions():
    response = make_response(
        [cell("11/03/2026", "5815", ["Baixar Regular", "Baixar Suplementar"])]
    )

    items = list(make_spider().parse_page_result(response))

    assert [item["file_urls"] for item in items] == [
        ["https://sga.aracaju.se.gov.br/diarios/5815.pdf"],
        ["https://sga.aracaju.se.gov.br/diarios/5815S.pdf"],
    ]
    assert [item["is_extra_edition"] for item in items] == [False, True]


def test_editions_outside_date_range_are_ignored():
    response = make_response([cell("28/02/2026", "5800"), cell("02/03/2026", "5801")])

    items = list(make_spider().parse_page_result(response))

    assert [item["edition_number"] for item in items] == ["5801"]


def test_next_page_request_keeps_form_and_asks_next_page():
    pager = (
        '<div class="rich-datascr" id="form:table:scroller"><table><tbody><tr>'
        '<td class="rich-datascr-act">1</td><td class="rich-datascr-inact">2</td>'
        "</tr></tbody></table></div>"
    )
    response = make_response([cell("31/03/2026", "5828")], pager)

    results = list(make_spider().parse_page_result(response))
    requests = [r for r in results if isinstance(r, Request)]

    assert len(requests) == 1
    body = requests[0].body.decode()
    assert "form%3Atable%3Ascroller=2" in body
    assert "ajaxSingle=form%3Atable%3Ascroller" in body
    assert "formPesquisarDiario%3Aj_id_26=2026" in body


def test_last_page_does_not_request_more_pages():
    pager = (
        '<div class="rich-datascr" id="form:table:scroller"><table><tbody><tr>'
        '<td class="rich-datascr-inact">1</td><td class="rich-datascr-act">2</td>'
        "</tr></tbody></table></div>"
    )
    response = make_response([cell("31/03/2026", "5828")], pager)

    results = list(make_spider().parse_page_result(response))

    assert not [r for r in results if isinstance(r, Request)]
