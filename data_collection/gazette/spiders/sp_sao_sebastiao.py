import re

from dateparser import parse as dateparser_parse
from scrapy.http import HtmlResponse
from scrapy.selector.unified import Selector

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class SpSaoSebastiaoSpider(BaseGazetteSpider):
    TERRITORY_ID = "3550704"
    name = "sp_sao_sebastiao"
    allowed_domains = ["saosebastiao.sp.gov.br"]

    BASE_URL = "http://www.saosebastiao.sp.gov.br"

    start_urls = [f"{BASE_URL}/doem.asp"]

    def get_pdf_url(self, gazette_node: Selector) -> str:
        path = gazette_node.css("::attr(href)").get()
        return f"{self.BASE_URL}/{path}"

    def get_edition_number(self, gazette_node: Selector) -> str:
        text = gazette_node.css("::text").get()
        return re.search(r"\d+", text).group()

    def get_pdf_date(self, url: str) -> str:
        date = re.search(r"\d{8}", url).group()
        return dateparser_parse(date, ["%Y%m%d"]).date()

    def parse(self, response: HtmlResponse) -> None:
        for gazette_node in response.css(".document a"):
            gazette_url = self.get_pdf_url(gazette_node)
            gazette_date = self.get_pdf_date(gazette_url)
            gazette_edition_number = self.get_edition_number(gazette_node)

            yield Gazette(
                date=gazette_date,
                territory_id=self.TERRITORY_ID,
                edition_number=gazette_edition_number,
                file_urls=[gazette_url],
                is_extra_edition=False,
                power="executive",
            )
