import asyncio
import json
from datetime import date

import pytest
from scrapy.http import Request, TextResponse

from gazette.spiders.rs.rs_porto_alegre import RsPortoAlegreSpider


async def collect_start_requests(spider):
    return [request async for request in spider.start()]


def make_api_response(data):
    url = (
        f"{RsPortoAlegreSpider.API_BASE_URL}"
        "/api/diarios/busca-por-mes-agrupada?mes=5&ano=2011"
    )
    request = Request(url)
    return TextResponse(
        url=url,
        request=request,
        body=json.dumps(data).encode(),
        encoding="utf-8",
    )


def test_start_builds_one_request_per_month():
    spider = RsPortoAlegreSpider(start="2026-06-15", end="2026-08-02")

    requests = asyncio.run(collect_start_requests(spider))

    assert [request.url.rsplit("?", 1)[-1] for request in requests] == [
        "mes=6&ano=2026",
        "mes=7&ano=2026",
        "mes=8&ano=2026",
    ]


def test_start_argument_uses_base_spider_override_behavior():
    spider = RsPortoAlegreSpider(start="2011-05-01", end="2011-05-03")

    requests = asyncio.run(collect_start_requests(spider))

    assert RsPortoAlegreSpider.start_date == date(2011, 5, 2)
    assert spider.start_date == date(2011, 5, 1)
    assert len(requests) == 1
    assert requests[0].url.endswith(
        "/api/diarios/busca-por-mes-agrupada?mes=5&ano=2011"
    )


def test_parse_api_month_filters_dates_and_keeps_each_publication():
    spider = RsPortoAlegreSpider(start="2011-05-01", end="2011-05-03")
    response = make_api_response(
        {
            "executivo": [
                {
                    "data": "02/05/2011",
                    "publicacoes": [
                        {
                            "idEdicao": 217,
                            "numeroEdicao": 4003,
                            "isExtra": False,
                            "linkDownload": (
                                "/api/diarios/edicao/217/download?tipo=executivo"
                            ),
                        },
                        {
                            "idEdicao": 218,
                            "numeroEdicao": 4003,
                            "isExtra": True,
                            "linkDownload": (
                                "/api/diarios/edicao/218/download?tipo=executivo"
                            ),
                        },
                    ],
                },
                {
                    "data": "04/05/2011",
                    "publicacoes": [
                        {
                            "idEdicao": 220,
                            "numeroEdicao": 4005,
                            "isExtra": False,
                            "linkDownload": (
                                "/api/diarios/edicao/220/download?tipo=executivo"
                            ),
                        }
                    ],
                },
            ],
            "legislativo": [
                {
                    "data": "03/05/2011",
                    "publicacoes": [
                        {
                            "idEdicao": 219,
                            "numeroEdicao": 4004,
                            "isExtra": False,
                            "linkDownload": (
                                "/api/diarios/edicao/219/download?tipo=legislativo"
                            ),
                        }
                    ],
                }
            ],
        }
    )

    gazettes = list(spider.parse_api_month(response))

    assert len(gazettes) == 3
    assert [gazette["edition_number"] for gazette in gazettes] == [4003, 4003, 4004]
    assert [str(gazette["date"]) for gazette in gazettes] == [
        "2011-05-02",
        "2011-05-02",
        "2011-05-03",
    ]
    assert [gazette["is_extra_edition"] for gazette in gazettes] == [
        False,
        True,
        False,
    ]
    assert [gazette["power"] for gazette in gazettes] == [
        "executive",
        "executive",
        "legislative",
    ]
    assert gazettes[0]["file_urls"] == [
        f"{spider.API_BASE_URL}/api/diarios/edicao/217/download?tipo=executivo"
    ]


@pytest.mark.parametrize(
    "data",
    [
        {"legislativo": []},
        {"executivo": []},
        {"executivo": [{"data": "02/05/2011", "publicacoes": []}]},
        {"executivo": [{"data": "02/05/2011"}]},
    ],
)
def test_parse_api_month_ignores_missing_or_empty_groups(data):
    spider = RsPortoAlegreSpider(start="2011-05-02", end="2011-05-03")

    assert list(spider.parse_api_month(make_api_response(data))) == []


@pytest.mark.parametrize(
    "publication",
    [
        {"idEdicao": 217, "numeroEdicao": 4003, "isExtra": False},
        {
            "idEdicao": 217,
            "numeroEdicao": 4003,
            "isExtra": False,
            "linkDownload": None,
        },
    ],
)
def test_parse_api_month_ignores_publication_without_download_link(publication):
    spider = RsPortoAlegreSpider(start="2011-05-02", end="2011-05-03")
    response = make_api_response(
        {"executivo": [{"data": "02/05/2011", "publicacoes": [publication]}]}
    )

    assert list(spider.parse_api_month(response)) == []


@pytest.mark.parametrize(
    ("link_download", "expected_url"),
    [
        (
            "/api/diarios/edicao/217/download?tipo=executivo",
            f"{RsPortoAlegreSpider.API_BASE_URL}"
            "/api/diarios/edicao/217/download?tipo=executivo",
        ),
        (
            "api/diarios/edicao/217/download?tipo=executivo",
            f"{RsPortoAlegreSpider.API_BASE_URL}"
            "/api/diarios/edicao/217/download?tipo=executivo",
        ),
        (
            "https://example.com/diario.pdf",
            "https://example.com/diario.pdf",
        ),
    ],
)
def test_parse_api_month_builds_download_url(link_download, expected_url):
    spider = RsPortoAlegreSpider(start="2011-05-02", end="2011-05-03")
    response = make_api_response(
        {
            "executivo": [
                {
                    "data": "02/05/2011",
                    "publicacoes": [
                        {
                            "idEdicao": 217,
                            "numeroEdicao": 4003,
                            "isExtra": False,
                            "linkDownload": link_download,
                        }
                    ],
                }
            ]
        }
    )

    gazettes = list(spider.parse_api_month(response))

    assert len(gazettes) == 1
    assert gazettes[0]["file_urls"] == [expected_url]
