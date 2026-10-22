import json

from scrapy.http import TextResponse

from gazette.spiders.ap.ap_santana import ApSantanaSpider


def make_response(payload):
    return TextResponse(
        url=ApSantanaSpider.start_urls[0],
        body=json.dumps({"data": payload}).encode("utf-8"),
        encoding="utf-8",
    )


def test_parse_downloads_google_drive_files_instead_of_viewer_page():
    spider = ApSantanaSpider(start="2019-01-01", end="2022-12-31")
    payload = [
        {
            "data": "08/01/2019",
            "arquivo": (
                '<a href="https://drive.google.com/open?id=1ArWubzYhzf4GObRT63j9r3kyoBNE_qDk"'
                ">Baixar</a>"
            ),
        },
        {
            "data": "15/01/2019",
            "arquivo": (
                '<a href="https://drive.google.com/uc?id=1Bx2_cD-3&amp;export=download"'
                ">Baixar</a>"
            ),
        },
        {
            "data": "15/06/2021",
            "arquivo": (
                '<a href="https://drive.google.com/file/d/1Cy3_dE-4/view?usp=sharing'
                '&amp;resourcekey=0-AbC_d-E">Baixar</a>'
            ),
        },
        {
            "data": "03/01/2022",
            "arquivo": (
                '<a href="https://www.santana.ap.gov.br/wp-content/uploads/2022/01/'
                'dom.pdf">Baixar</a>'
            ),
        },
    ]

    gazettes = list(spider.parse(make_response(payload)))

    download_url = "https://drive.google.com/uc?export=download&id="
    assert [gazette["file_urls"] for gazette in gazettes] == [
        [f"{download_url}1ArWubzYhzf4GObRT63j9r3kyoBNE_qDk"],
        [f"{download_url}1Bx2_cD-3"],
        [f"{download_url}1Cy3_dE-4&resourcekey=0-AbC_d-E"],
        ["https://www.santana.ap.gov.br/wp-content/uploads/2022/01/dom.pdf"],
    ]
