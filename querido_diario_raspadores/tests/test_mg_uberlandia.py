from scrapy.http import HtmlResponse

from gazette.spiders.mg.mg_uberlandia import MgUberlandiaSpider


def test_intermediary_page_downloads_pdf_without_zyte_proxy():
    spider = MgUberlandiaSpider()
    response = HtmlResponse(
        url="https://www.uberlandia.mg.gov.br/diario/7436/",
        body=b'<script>location="https://docs.uberlandia.mg.gov.br/7436.pdf";</script>',
    )

    gazette = next(
        spider.intermediary_page(
            response,
            {
                "date": "2026-09-11",
                "edition_number": "7436",
                "is_extra_edition": False,
            },
        )
    )

    assert gazette["file_requests"][0].url == (
        "https://docs.uberlandia.mg.gov.br/7436.pdf"
    )
    assert gazette["file_requests"][0].meta == {"dont_proxy": True}
