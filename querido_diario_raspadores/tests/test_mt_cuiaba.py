import json
from datetime import date

from scrapy.http import TextResponse

from gazette.spiders.mt.mt_cuiaba import MtCuiabaSpider


def make_response(editions):
    return TextResponse(
        url=f"{MtCuiabaSpider.BASE_URL}/published/1990/12",
        body=json.dumps({"status": "success", "editions": editions}).encode("utf-8"),
        encoding="utf-8",
    )


def make_edition(edition_id, number, type_name, suplement=False):
    return {
        "id": edition_id,
        "number": number,
        "edition_type_name": type_name,
        "suplement": suplement,
        "publication_date": "1990-12-03T03:00:00.000000Z",
    }


def test_parse_only_yields_the_municipal_gazette():
    spider = MtCuiabaSpider()
    response = make_response(
        [
            make_edition(7746, 1, "Gazeta Municipal de Cuiabá"),
            make_edition(9080, 20568, "Diário Oficial do Mato Grosso"),
            make_edition(1, 10, "Diário Oficial do Tribunal de Contas"),
            make_edition(7747, 1, "Gazeta Municipal de Cuiabá", suplement=True),
        ]
    )

    items = list(spider.parse(response))

    assert [item["file_urls"] for item in items] == [
        [f"{MtCuiabaSpider.BASE_URL}/downloadPdf/7746"],
        [f"{MtCuiabaSpider.BASE_URL}/downloadPdf/7747"],
    ]
    assert [item["is_extra_edition"] for item in items] == [False, True]
    assert all(item["date"] == date(1990, 12, 3) for item in items)
    assert all(item["edition_number"] == 1 for item in items)
