import re
from datetime import date

import scrapy
from dateutil.rrule import DAILY, rrule

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider

RE_MAX_PAGE_NUM = re.compile(r"\d+ de (\d+)")
FULL_MONTH_NAME = {
    1: "Janeiro",
    2: "Fevereiro",
    3: "Março",
    4: "Abril",
    5: "Maio",
    6: "Junho",
    7: "Julho",
    8: "Agosto",
    9: "Setembro",
    10: "Outubro",
    11: "Novembro",
    12: "Dezembro",
}


class SpSaoPauloSpider(BaseGazetteSpider):
    TERRITORY_ID = "3550308"
    BASE_URL = "http://diariooficial.imprensaoficial.com.br"
    allowed_domains = ["diariooficial.imprensaoficial.com.br"]
    name = "sp_sao_paulo"
    start_date = date(2017, 6, 1)

    def start_requests(self):
        for day in rrule(freq=DAILY, dtstart=self.start_date, until=self.end_date):
            url = f"{self.BASE_URL}/nav_v6/header.asp?txtData={day.strftime('%d/%m/%Y')}&cad=1"
            yield scrapy.Request(url, cb_kwargs=dict(day=day.date()))

    def get_max_page(self, response):
        page_txt = response.css("span.form-text::text").get()

        try:
            max_page = int(RE_MAX_PAGE_NUM.search(page_txt).group(1))
        except TypeError:
            max_page = None

        return max_page

    def parse(self, response, day):
        max_page = self.get_max_page(response)
        if not max_page:
            return
        day_url = (
            f"{self.BASE_URL}"
            "/doflash/prototipo"
            f"/{day.strftime('%Y')}"
            f"/{FULL_MONTH_NAME[day.month]}"
            f"/{day.strftime('%d')}"
            "/cidade/pdf"
        )
        urls = [f"{day_url}/pg_{page:04}.pdf" for page in range(1, max_page + 1)]

        yield Gazette(
            date=day,
            file_urls=urls,
            is_extra_edition=False,
            territory_id=self.TERRITORY_ID,
            power="executive",
        )
