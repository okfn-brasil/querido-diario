from calendar import monthrange
from datetime import date

from dateparser import parse
from dateutil.rrule import MONTHLY, rrule
from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class PaAnanindeuaSpider(BaseGazetteSpider):

    TERRITORY_ID = "1500800"
    name = "pa_ananindeua"
    allowed_domains = ["ananindeua.pa.gov.br"]
    url_base = "https://www.ananindeua.pa.gov.br/diario_oficial.asp?titulo={}&dataini={}&datafim={}&order=1&go=Buscar&bt_buscar=buscar&num_rows=31&pag=1"
    start_date = date(2008, 1, 21)

    FILE_ELEMENT_CSS = "div.item_lic div.list-group a.list-group-item::attr(href)"
    DATE_ELEMENT_CSS = "div.item_lic div.d-flex div.small::text"
    DATE_FORMAT = "%d/%m/%Y"

    def start_requests(self):
        initial_date = date(self.start_date.year, self.start_date.month, 1)
        for monthly_date in rrule(
            freq=MONTHLY, dtstart=initial_date, until=self.end_date
        ):
            month_range = monthrange(monthly_date.year, monthly_date.month)
            month_start = monthly_date.replace(day=1).strftime(self.DATE_FORMAT)
            month_end = monthly_date.replace(day=month_range[1]).strftime(
                self.DATE_FORMAT
            )
            url = self.url_base.format(monthly_date.year, month_start, month_end)
            yield Request(url)

    def parse(self, response):
        file_urls = response.css(self.FILE_ELEMENT_CSS).extract()
        dates = response.css(self.DATE_ELEMENT_CSS).extract()

        for date_str, file_url in zip(dates, file_urls):
            date = parse(date_str.split(": ")[1], languages=["pt"]).date()
            url = response.urljoin(file_url)
            yield Gazette(
                date=date,
                file_urls=[url],
                is_extra_edition="extra" in url.lower(),
                territory_id=self.TERRITORY_ID,
                power="executive",
            )
