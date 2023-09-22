from datetime import date, datetime

import scrapy
from dateutil.rrule import MONTHLY, rrule

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RjBelfordRoxoSpider(BaseGazetteSpider):
    TERRITORY_ID = "3300456"
    name = "rj_belford_roxo"
    allowed_domains = ["transparencia.prefeituradebelfordroxo.rj.gov.br"]
    BASE_URL = "https://transparencia.prefeituradebelfordroxo.rj.gov.br/webrun/WEB-ObterAnexo.rule?sys=LAI&codigo={ATTACHMENT_CODE}"

    start_date = date(2019, 1, 2)

    def start_requests(self):
        url = "https://transparencia.prefeituradebelfordroxo.rj.gov.br/diario_oficial_get.php"
        initial_date = date(self.start_date.year, self.start_date.month, 1)

        for monthly_date in rrule(
            freq=MONTHLY, dtstart=initial_date, until=self.end_date
        ):
            month_year = monthly_date.strftime("%m/%Y").lstrip("0")  # like 9/2022
            yield scrapy.FormRequest(
                url=url,
                formdata={"mesano": month_year},
            )

    def parse(self, response):
        for gazette_data in response.json():
            raw_gazette_date = gazette_data["Data_Formatada"]
            gazette_date = datetime.strptime(raw_gazette_date, "%d/%m/%Y").date()
            if gazette_date < self.start_date or self.end_date < gazette_date:
                continue
            gazette_code = gazette_data["Codigo_ANEXO"]
            gazette_edition_number = gazette_data["ANEXO"]
            gazette_url = self.BASE_URL.format(ATTACHMENT_CODE=gazette_code)

            yield Gazette(
                date=gazette_date,
                edition_number=gazette_edition_number,
                file_urls=[gazette_url],
                is_extra_edition=False,
                power="executive",
            )
