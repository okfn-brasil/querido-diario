import re
from datetime import datetime

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider
from gazette.utils.dates import monthly_sequence


class BaseModernizacaoSpider(BaseGazetteSpider):
    power = "executive_legislative"
    ver_subpath = "ver20230623"
    filter_endpoint = "diario_oficial_get"
    edition_endpoint = "WEB-ObterAnexo.rule"

    custom_settings = {
        "CONCURRENT_REQUESTS": 4,
        "DOWNLOAD_DELAY": 0.75,
    }

    def start_requests(self):
        domain = self.allowed_domains[0]
        base_url = f"https://{domain}/{self.filter_endpoint}.php"

        for month_year in monthly_sequence(
            self.start_date, self.end_date, format="%m/%Y"
        ):
            yield scrapy.FormRequest(
                url=base_url,
                formdata={"mesano": month_year.lstrip("0")},
            )

    def parse(self, response):
        for gazette_data in response.json():
            raw_gazette_date = gazette_data["Data_Formatada"]
            gazette_date = datetime.strptime(raw_gazette_date, "%d/%m/%Y").date()
            if gazette_date > self.end_date:
                continue
            if gazette_date < self.start_date:
                return

            gazette_code = gazette_data["Codigo_ANEXO"]
            gazette_url = response.urljoin(
                f"diario_oficial_get_anexo.php?codigo={gazette_code}"
            )

            raw_edition_number = gazette_data["ANEXO"]
            gazette_edition_number = re.search(r"\d+", raw_edition_number)

            if gazette_edition_number is None:
                gazette_edition_number = ""
            else:
                gazette_edition_number = gazette_edition_number.group(0)

            is_extra_edition = bool(
                re.search(r"extra|supl|ee|esp", raw_edition_number, re.IGNORECASE)
            )

            yield Gazette(
                date=gazette_date,
                edition_number=gazette_edition_number,
                file_urls=[gazette_url],
                is_extra_edition=is_extra_edition,
                power=self.power,
            )
