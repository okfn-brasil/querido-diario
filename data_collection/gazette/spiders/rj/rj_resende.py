import re
from datetime import date

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RjResendeSpider(BaseGazetteSpider):
    name = "rj_resende"
    TERRITORY_ID = "3302254"
    allowed_domains = ["resende.rj.gov.br"]
    start_date = date(2009, 1, 1)
    BASE_URL = (
        "https://resende.rj.gov.br/blogtransparencia/page/boletim_oficialselect.asp"
    )

    def start_requests(self):
        for year in range(self.end_date.year, self.start_date.year - 1, -1):
            payload = {"ano": str(year), "funcao": "buscaBo"}
            yield scrapy.FormRequest(
                url=self.BASE_URL,
                formdata=payload,
                meta={"year": year},
            )

    def parse(self, response):
        year = response.meta["year"]
        gazettes = response.xpath("//option[starts-with(@value, 'Boletim_')]")

        for gazette in gazettes:
            gazette_filename = gazette.xpath("@value").get()
            gazette_text = gazette.xpath("text()").get("").strip()

            full_url = f"https://resende.rj.gov.br/conteudo/boletim_oficial/{year}/{gazette_filename}"

            match = re.search(r"N[°º\.]*\s*(\d+)\s*-\s*(\d{2})/(\d{2})", gazette_text)
            if not match:
                continue

            edition_number, day, month = match.groups()
            gazette_date = date(year, int(month), int(day))

            if gazette_date > self.end_date:
                continue
            if gazette_date < self.start_date:
                return

            yield Gazette(
                date=gazette_date,
                edition_number=edition_number,
                is_extra_edition=False,
                file_urls=[full_url],
                power="executive_legislative",
            )
