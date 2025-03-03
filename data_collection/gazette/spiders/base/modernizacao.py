import re
from datetime import date, datetime

import scrapy
from dateutil.rrule import MONTHLY, rrule

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


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
        initial_date = date(self.start_date.year, self.start_date.month, 1)

        for monthly_date in rrule(
            freq=MONTHLY, dtstart=initial_date, until=self.end_date
        ):
            month_year = monthly_date.strftime("%m/%Y").lstrip("0")
            yield scrapy.FormRequest(
                url=base_url,
                formdata={"mesano": month_year},
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
                f"{self.ver_subpath}/{self.edition_endpoint}?sys=LAI&codigo={gazette_code}"
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
