import json
from datetime import date

from scrapy.http import TextResponse

from gazette.spiders.base.dosp import BaseDospSpider


class DospSpiderForTest(BaseDospSpider):
    TERRITORY_ID = "0000000"
    name = "dosp_test"
    start_date = date(2026, 9, 1)
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/example"]


def make_response(body):
    return TextResponse(
        url="https://dosp.com.br/api/index.php/dioe.js/1",
        body=body.encode("utf-8"),
        encoding="utf-8",
    )


def api_payload():
    return {
        "data": [
            {
                "data": "2026-09-10",
                "edicao_do": "123",
                "flag_extra": 0,
                "iddo": 42,
            }
        ]
    }


def test_parse_json_accepts_current_raw_javascript_response():
    spider = DospSpiderForTest(end="2026-09-12")
    response = make_response(f"parseResponse({json.dumps(api_payload())});")

    gazettes = list(spider.parse_json(response))

    assert len(gazettes) == 1
    assert gazettes[0]["date"] == date(2026, 9, 10)
    assert gazettes[0]["file_urls"] == ["https://dosp.com.br/exibe_do.php?i=NDI=.pdf"]


def test_parse_json_keeps_compatibility_with_legacy_paragraph_response():
    spider = DospSpiderForTest(end="2026-09-12")
    response = make_response(f"<p>parseResponse({json.dumps(api_payload())});</p>")

    assert len(list(spider.parse_json(response))) == 1
