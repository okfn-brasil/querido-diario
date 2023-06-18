import re
from datetime import datetime

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class AdminlteGazetteSpider(BaseGazetteSpider):
    """
    Base spider for cities using the Framework AdminLTE as design system.

    To set the date_column and file_url_column, start counting from zero.
    """

    def start_requests(self):
        url = f"http://diariooficial.{self.city_domain}/pesquisa/"

        start_date = self.start_date.strftime("%Y-%m-%d")
        end_date = self.end_date.strftime("%Y-%m-%d")

        formdata = {
            "data_inicial": start_date,
            "data_final": end_date,
            "pagina": "",
            "opcao": "opcao_b",
        }

        yield scrapy.FormRequest(
            url,
            method="POST",
            formdata=formdata,
            callback=self.get_page_number,
            cb_kwargs={"start_date": start_date, "end_date": end_date, "url": url},
        )

    def get_page_number(self, response, start_date, end_date, url):
        last_page = response.xpath("(//button[@id='pagina'])[last()]/@value").get()
        last_page = re.search(r"^(.*?)&", last_page).group(1)

        stop = int(last_page)

        for page in range(0, stop):
            formdata = {
                "data_inicial": start_date,
                "data_final": end_date,
                "pagina": str(page + 1),
                "opcao": "opcao_b",
            }

            yield scrapy.FormRequest(
                url, method="POST", formdata=formdata, callback=self.parse
            )

    def parse(self, response):
        gazettes = response.xpath("//table/tbody/tr")

        for gazette in gazettes:
            edition_number = gazette.xpath("./th/text()").get()
            file_name = gazette.xpath(
                f"./td[{self.file_url_column}]/div/div/a/@href"
            ).get()
            edition_type = re.search(r"/([^/]+)/[^/]+$", file_name).group(1)
            file_name = re.search(r"/([^/]+)$", file_name).group(1)
            file_url = f"http://diariooficial.{self.city_domain}/arquivos/{edition_type}/{file_name}"

            date = gazette.xpath(f"./td[{self.date_column}]/text()").get()
            date = datetime.strptime(date, "%d/%m/%Y").date()

            yield Gazette(
                date=date,
                edition_number=edition_number,
                file_urls=[file_url],
                is_extra_edition=(edition_type == "Edição Extra"),
                power="executive",
            )
