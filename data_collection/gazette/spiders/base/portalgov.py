import re
from datetime import datetime as dt

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class BasePortalGovSpider(BaseGazetteSpider):
    power = "executive"

    def start_requests(self):
        yield scrapy.FormRequest(
            url=f"https://{self.domain}/controllers/diario_oficial/class_diario.php",
            formdata={
                "func": "5",
                "param": "1",
            },
        )

    def parse(self, response):
        for gazette_data in response.json():
            raw_gazette_date = gazette_data["data"]
            gazette_date = dt.strptime(raw_gazette_date, "%d/%m/%Y").date()
            if gazette_date > self.end_date:
                continue
            if gazette_date < self.start_date:
                return

            gazette_desc = gazette_data["descricao"]
            gazette_edition = gazette_data["numero"]
            gazette_edition_number = re.search(r"\d+", gazette_edition).group(0)
            is_extra_edition = bool(
                re.search(r"extra|supl", gazette_edition + gazette_desc, re.IGNORECASE)
            )

            gazette_url = f"https://{self.domain}/arquivos/diario_oficial/{gazette_data['arquivo']}"

            yield Gazette(
                date=gazette_date,
                edition_number=gazette_edition_number,
                file_urls=[gazette_url],
                is_extra_edition=is_extra_edition,
                power=self.power,
            )
