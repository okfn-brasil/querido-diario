import asyncio
import json
from datetime import date

import pytest
from scrapy.http import HtmlResponse, Request, TextResponse

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


def make_html_response(url, body):
    request = Request(url)
    return HtmlResponse(
        url=url,
        request=request,
        body=body.encode(),
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


def test_start_builds_archive_and_api_requests_across_source_transition():
    spider = RsPortoAlegreSpider(start="2010-12-30", end="2011-05-03")

    requests = asyncio.run(collect_start_requests(spider))

    assert [request.url for request in requests] == [
        spider.ARCHIVE_YEAR_URL.format(year=2010),
        spider.ARCHIVE_YEAR_URL.format(year=2011),
        (f"{spider.API_BASE_URL}/api/diarios/busca-por-mes-agrupada" "?mes=5&ano=2011"),
    ]
    assert requests[0].cb_kwargs == {
        "period_start": date(2010, 12, 30),
        "period_end": date(2010, 12, 31),
    }
    assert requests[1].cb_kwargs == {
        "period_start": date(2011, 1, 1),
        "period_end": date(2011, 4, 29),
    }


def test_start_uses_archive_url_override_for_2003():
    spider = RsPortoAlegreSpider(start="2003-01-01", end="2003-12-31")

    requests = asyncio.run(collect_start_requests(spider))

    assert len(requests) == 1
    assert requests[0].url.endswith("/diario-oficial-de-porto-alegre-de-2003-2")


def test_start_argument_uses_base_spider_override_behavior():
    spider = RsPortoAlegreSpider(start="2011-05-01", end="2011-05-03")

    requests = asyncio.run(collect_start_requests(spider))

    assert RsPortoAlegreSpider.start_date == date(1995, 3, 15)
    assert spider.start_date == date(2011, 5, 1)
    assert len(requests) == 1
    assert requests[0].url.endswith(
        "/api/diarios/busca-por-mes-agrupada?mes=5&ano=2011"
    )


def test_parse_archive_year_follows_full_listing():
    spider = RsPortoAlegreSpider(start="2010-01-01", end="2010-12-31")
    response = make_html_response(
        spider.ARCHIVE_YEAR_URL.format(year=2010),
        """
        <html><body>
          <a href="/index.php/informationobject/browse?ancestor=113236&amp;onlyMedia=1">
            Exibir tudo
          </a>
        </body></html>
        """,
    )

    requests = list(
        spider.parse_archive_year(
            response,
            period_start=date(2010, 1, 1),
            period_end=date(2010, 12, 31),
        )
    )

    assert len(requests) == 1
    assert requests[0].callback == spider.parse_archive_list
    assert "view=table" in requests[0].url
    assert requests[0].cb_kwargs == {
        "period_start": date(2010, 1, 1),
        "period_end": date(2010, 12, 31),
    }


def test_parse_archive_list_handles_standard_extra_second_edition_and_pagination():
    spider = RsPortoAlegreSpider(start="2010-03-01", end="2010-03-31")
    response = make_html_response(
        "https://atom2.procempa.com.br/index.php/informationobject/browse"
        "?ancestor=113236&onlyMedia=1",
        """
        <html><body>
          <a href="/index.php/dopa-edicao-no-3-712-de-01-03-2010">
            DOPA 2ª edição Nº 3.712 de 01/03/2010
          </a>
          <a href="/index.php/dopa-edicao-extra-no-3-733-de-30-03-2010">
            DOPA edição extra Nº 3.733 de 30/03/2010
          </a>
          <a href="/index.php/dopa-edicao-no-3-735-de-01-04-2010">
            DOPA edição Nº 3.735 de 01/04/2010
          </a>
          <a href="?ancestor=113236&amp;onlyMedia=1&amp;page=2">Próximo</a>
        </body></html>
        """,
    )

    requests = list(
        spider.parse_archive_list(
            response,
            period_start=date(2010, 3, 1),
            period_end=date(2010, 3, 31),
        )
    )

    edition_requests = [
        request for request in requests if request.callback == spider.parse_archive_item
    ]
    next_requests = [
        request for request in requests if request.callback == spider.parse_archive_list
    ]

    assert len(edition_requests) == 2
    assert edition_requests[0].cb_kwargs == {
        "date": date(2010, 3, 1),
        "edition_number": 3712,
        "is_extra_edition": False,
    }
    assert edition_requests[1].cb_kwargs == {
        "date": date(2010, 3, 30),
        "edition_number": 3733,
        "is_extra_edition": True,
    }
    assert len(next_requests) == 1
    assert "page=2" in next_requests[0].url


def test_parse_archive_list_handles_title_without_edition():
    spider = RsPortoAlegreSpider(start="1995-05-02", end="1995-05-02")
    response = make_html_response(
        "https://atom2.procempa.com.br/index.php/informationobject/browse",
        """
        <html><body>
          <a href="/index.php/dopa-no-32-de-02-05-1995">
            DOPA Nº 32 de 02/05/1995
          </a>
        </body></html>
        """,
    )

    requests = list(
        spider.parse_archive_list(
            response,
            period_start=date(1995, 5, 2),
            period_end=date(1995, 5, 2),
        )
    )

    assert len(requests) == 1
    assert requests[0].callback == spider.parse_archive_item
    assert requests[0].cb_kwargs == {
        "date": date(1995, 5, 2),
        "edition_number": 32,
        "is_extra_edition": False,
    }


def test_parse_archive_item_builds_gazette_from_matrix_pdf():
    spider = RsPortoAlegreSpider(start="2010-03-30", end="2010-03-30")
    response = make_html_response(
        "https://atom2.procempa.com.br/index.php/"
        "dopa-edicao-extra-no-3-733-de-30-03-2010",
        """
        <html><body>
          <a href="/uploads/r/archive/db5a-30marco10_extra.pdf">
            db5a-30marco10_extra.pdf
          </a>
          <a href="/uploads/r/archive/db5a-30marco10_extra_142.jpg">
            thumbnail
          </a>
        </body></html>
        """,
    )

    gazettes = list(
        spider.parse_archive_item(
            response,
            date=date(2010, 3, 30),
            edition_number=3733,
            is_extra_edition=True,
        )
    )

    assert len(gazettes) == 1
    assert gazettes[0]["date"] == date(2010, 3, 30)
    assert gazettes[0]["edition_number"] == 3733
    assert gazettes[0]["is_extra_edition"] is True
    assert gazettes[0]["power"] == "executive_legislative"
    assert gazettes[0]["file_urls"] == [
        "https://atom2.procempa.com.br/uploads/r/archive/db5a-30marco10_extra.pdf"
    ]


@pytest.mark.parametrize(
    ("title", "expected"),
    [
        (
            "DOPA Nº 32 de 02/05/1995",
            (date(1995, 5, 2), 32, False),
        ),
        (
            "DOPA edição Nº 3.675 de 04/01/2010",
            (date(2010, 1, 4), 3675, False),
        ),
        (
            "DOPA edição extra Nº 3.733 de 30/03/2010",
            (date(2010, 3, 30), 3733, True),
        ),
        (
            "DOPA 2ª edição Nº 3.712 de 01/03/2010",
            (date(2010, 3, 1), 3712, False),
        ),
    ],
)
def test_extract_archive_metadata(title, expected):
    spider = RsPortoAlegreSpider(start="2010-01-01", end="2010-12-31")

    assert spider._extract_archive_metadata(title) == expected


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
    "date_group",
    [
        {"publicacoes": []},
        {"data": None, "publicacoes": []},
        {"data": "", "publicacoes": []},
    ],
)
def test_parse_api_month_ignores_date_group_without_date(date_group):
    spider = RsPortoAlegreSpider(start="2011-05-02", end="2011-05-03")
    response = make_api_response({"executivo": [date_group]})

    assert list(spider.parse_api_month(response)) == []


@pytest.mark.parametrize(
    "raw_date",
    ["31/13/2011", "not-a-date", 20110502],
)
def test_parse_api_month_ignores_date_group_with_invalid_date(raw_date):
    spider = RsPortoAlegreSpider(start="2011-05-02", end="2011-05-03")
    response = make_api_response(
        {
            "executivo": [
                {
                    "data": raw_date,
                    "publicacoes": [
                        {
                            "idEdicao": 217,
                            "numeroEdicao": 4003,
                            "isExtra": False,
                            "linkDownload": (
                                "/api/diarios/edicao/217/download?tipo=executivo"
                            ),
                        }
                    ],
                }
            ]
        }
    )

    assert list(spider.parse_api_month(response)) == []


def test_parse_api_month_ignores_publication_without_edition_number_but_keeps_others():
    spider = RsPortoAlegreSpider(start="2011-05-02", end="2011-05-03")
    response = make_api_response(
        {
            "executivo": [
                {
                    "data": "02/05/2011",
                    "publicacoes": [
                        {
                            "idEdicao": 217,
                            "isExtra": False,
                            "linkDownload": (
                                "/api/diarios/edicao/217/download?tipo=executivo"
                            ),
                        },
                        {
                            "idEdicao": 218,
                            "numeroEdicao": 4004,
                            "isExtra": False,
                            "linkDownload": (
                                "/api/diarios/edicao/218/download?tipo=executivo"
                            ),
                        },
                    ],
                }
            ]
        }
    )

    gazettes = list(spider.parse_api_month(response))

    assert len(gazettes) == 1
    assert gazettes[0]["edition_number"] == 4004


def test_parse_api_month_ignores_publication_without_is_extra_but_keeps_others():
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
                            "linkDownload": (
                                "/api/diarios/edicao/217/download?tipo=executivo"
                            ),
                        },
                        {
                            "idEdicao": 218,
                            "numeroEdicao": 4004,
                            "isExtra": False,
                            "linkDownload": (
                                "/api/diarios/edicao/218/download?tipo=executivo"
                            ),
                        },
                    ],
                }
            ]
        }
    )

    gazettes = list(spider.parse_api_month(response))

    assert len(gazettes) == 1
    assert gazettes[0]["edition_number"] == 4004


def test_parse_api_month_accepts_is_extra_false():
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
                            "linkDownload": (
                                "/api/diarios/edicao/217/download?tipo=executivo"
                            ),
                        }
                    ],
                }
            ]
        }
    )

    gazettes = list(spider.parse_api_month(response))

    assert len(gazettes) == 1
    assert gazettes[0]["is_extra_edition"] is False


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
