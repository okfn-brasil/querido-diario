import re
from datetime import date

import dateparser
from scrapy.http import FormRequest

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class MgBetimSpider(BaseGazetteSpider):
    name = "mg_betim"
    TERRITORY_ID = "3106705"
    start_urls = ["http://betim.mg.gov.br/orgaooficial/"]
    start_date = date(2008, 1, 1)
    end_date = date.today()

    def parse(self, response):
        yield FormRequest.from_response(
            response,
            formdata={
                "txtDataInicial": self.start_date.strftime("%d/%m/%Y"),
                "txtDataFinal": self.end_date.strftime("%d/%m/%Y"),
                "btnPesquisar": "Pesquisar",
            },
            callback=self.parse_gazettes,
        )

    def parse_gazettes(self, response):
        gazettes_links = response.xpath(
            '//table[@id="gdvEdicoes"]//a[contains(@href, ".pdf")]/@href'
        ).getall()  # .selector

        for href in gazettes_links:
            data = dateparser.parse(
                re.search(r"(\d{8})\.pdf", href).group(1), date_formats=["%d%m%Y"]
            ).date()
            edition_number = re.search(r"orgaooficial_\d+_(\d+)_", href).group(1)
            yield Gazette(
                date=data,
                file_urls=[response.urljoin(href)],
                edition_number=edition_number,
                power="executive_legislative",
            )

        yield from self.paginate(response)

    def paginate(self, response):
        current_page = response.xpath(
            "//table[@id='gdvEdicoes']//table//span/text()"
        ).get()
        if current_page is None:
            return

        next_page = "Page$" + str(int(current_page) + 1)
        has_next_page = response.xpath(
            f"//table[@id='gdvEdicoes']//table//a[contains(@href, '{next_page}')]"
        ).get()
        if has_next_page is not None:
            yield FormRequest.from_response(
                response,
                formdata={
                    "__EVENTTARGET": "gdvEdicoes",
                    "__EVENTARGUMENT": next_page,
                    "txtDataInicial": self.start_date.strftime("%d/%m/%Y"),
                    "txtDataFinal": self.end_date.strftime("%d/%m/%Y"),
                },
                callback=self.parse_gazettes,
            )
