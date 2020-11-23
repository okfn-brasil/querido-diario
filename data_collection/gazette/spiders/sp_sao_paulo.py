import locale
import re
from datetime import date, datetime

import scrapy
from dateutil.rrule import DAILY, rrule

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider

RE_MAX_PAGE_NUM = re.compile(r"\d+ de (\d+)")


class SpSaoPauloSpider(BaseGazetteSpider):
    TERRITORY_ID = "3550308"
    BASE_URL = "http://diariooficial.imprensaoficial.com.br"
    allowed_domains = ["diariooficial.imprensaoficial.com.br"]
    name = "sp_sao_paulo"
    start_date = date(2017, 6, 1)

    def start_requests(self):
        # Need to have the month's name in portuguese for the pdf url
        locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")
        for day in rrule(freq=DAILY, dtstart=self.start_date, until=date.today()):
            url = f"{self.BASE_URL}/nav_v6/header.asp?txtData={day.strftime('%d/%m/%Y')}&cad=1"
            yield scrapy.Request(url, cb_kwargs=dict(day=day.date()))

    def get_max_page(self, response):
        page_txt = response.css("span.form-text::text").get()

        try:
            max_page = int(RE_MAX_PAGE_NUM.search(page_txt).group(1))
        except:
            max_page = None

        return max_page

    def parse(self, response, day):
        max_page = self.get_max_page(response)
        if not max_page:
            return
        day_url = f"{self.BASE_URL}/doflash/prototipo/{day.strftime('%Y')}/{day.strftime('%B')}/{day.strftime('%d')}/cidade/pdf"
        urls = [f"{day_url}/pg_{page:04}.pdf" for page in range(1, max_page + 1)]

        yield Gazette(
            date=day,
            file_urls=urls,
            is_extra_edition=False,
            territory_id=self.TERRITORY_ID,
            power="executive",
            scraped_at=datetime.utcnow(),
        )
