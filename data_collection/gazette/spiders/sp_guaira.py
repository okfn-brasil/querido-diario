import datetime

from scrapy.http import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class SpGuairaSpider(BaseGazetteSpider):
    TERRITORY_ID = "3517406"
    name = "sp_guaira"
    allowed_domains = ["guaira.sp.gov.br"]
    start_urls = ["https://guaira.sp.gov.br/category/diarioficial/"]
    start_date = datetime.date(2013, 6, 19)

    def extract_edition_number(self, text):
        edition_number_raw = text.split(" ")[-1]
        edition_number = ""

        for char in edition_number_raw:
            if char.isdigit():
                edition_number += char
        return edition_number

    def extract_edition_number_extra(self, text):
        edition_number = ""

        for char in text:
            if char.isdigit():
                edition_number += char
        return edition_number

    def parse(self, response, current_page=1):

        lines = response.xpath('//div[@class="bloco-post-category-concursos"]')

        if not lines:
            return

        for row in lines:
            urls = row.xpath('div[@class="descricao-post-category-concursos"]/p/a')
            urls = urls.xpath("@href").getall()
            date = row.xpath('p[@class="data-post-category"]/text()').get()
            date = datetime.datetime.strptime(date, "%d/%m/%Y").date()
            edition_number_raw = row.xpath(
                'h4[@class="titulo-post-category"]/text()'
            ).get()
            edition_number = self.extract_edition_number(edition_number_raw)
            extra_edition = False

            if not edition_number:
                edition_number = self.extract_edition_number_extra(edition_number_raw)
                extra_edition = True

            if not urls:
                continue

            if date <= self.start_date:
                return

            yield Gazette(
                date=date,
                edition_number=edition_number,
                file_urls=urls,
                is_extra_edition=extra_edition,
                power="executive_legislative",
            )

        yield Request(
            f"https://guaira.sp.gov.br/category/diarioficial/page/{str(current_page)}",
            cb_kwargs=dict(current_page=current_page + 1),
        )
