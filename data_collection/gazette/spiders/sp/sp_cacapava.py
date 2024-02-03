import re
from datetime import date, datetime

from scrapy.http import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class SpCacapavaSpider(BaseGazetteSpider):
    TERRITORY_ID = "3508504"
    name = "sp_cacapava"
    allowed_domains = ["cacapava.sp.gov.br", "ecrie.com.br"]
    start_date = date(2021, 4, 27)
    custom_settings = {"DOWNLOAD_DELAY": 0.5, "RANDOMIZE_DOWNLOAD_DELAY": True}

    def start_requests(self):
        url = "https://cacapava.sp.gov.br/diario-oficial?"
        url += f'&dataDe={self.start_date.strftime("%d/%m/%Y")}'
        url += f'&dataAte={self.end_date.strftime("%d/%m/%Y")}'
        yield Request(url, callback=self.parse_info)

    def parse_info(self, response):
        base_url = response.url
        num_pages = response.css(".pagination__select option::text")[-1].get()
        for i in range(1, int(num_pages) + 1):
            yield Request(f"{base_url}&pagina={i}")

    def parse(self, response):
        for gazette in response.css(".list-item__info"):
            gazette_number = re.findall(
                "Edição nº (\d+)", gazette.css("h3::text").get()
            )[0]
            raw_date = re.findall("\d{2}/\d{2}/\d{4}", gazette.css("p::text").get())[0]
            gazette_date = datetime.strptime(raw_date, "%d/%m/%Y").date()
            gazette_url = gazette.css("a").attrib["href"]

            yield Gazette(
                date=gazette_date,
                edition_number=gazette_number,
                is_extra_edition=False,
                power="executive_legislative",
                file_urls=[gazette_url],
            )
