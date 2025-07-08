import re
from datetime import date, datetime as dt

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
class BaseRgSitesSpider(BaseGazetteSpider):
=======
class BaseRgSites(BaseGazetteSpider):
>>>>>>> 2d239c1 (Cria spider base rgsites #1245)
=======
class BaseRgSitesSpider(BaseGazetteSpider):
>>>>>>> 30a1d25 (ajeitando nome da classe e data inicial)
=======
class BaseRgSitesSpider(BaseGazetteSpider):
>>>>>>> 18d6b9e06c24e765d3cadcca5549893d0cd55934
    def start_requests(self):
        yield scrapy.Request(self.BASE_URL)

    def parse(self, response):
        month_after_end_date = date(self.end_date.year, self.end_date.month + 1, 1)
        years = response.css('div[role="tabpanel"]')
        for year in years:
            year_temp = year.css("::attr(id)").get()
            year_temp = int(year_temp.replace("tab_", ""))
            if year_temp not in range(self.start_date.year, self.end_date.year + 1):
                continue
            months = year.css("div.panel.panel-primary.rg-border-radius-none")
            months.reverse()
            for month in months:
                days = month.css("td.edicao")
                days.reverse()
                for day in days:
                    date_temp = day.css("span.visible-xs-inline-block::text").get()
                    date_temp = (
                        date_temp.strip()
                        .replace("\xa0", "")
                        .replace("(", "")
                        .replace(")", "")
                    )
                    date_temp = dt.strptime(date_temp, "%d/%m/%Y").date()

                    if date_temp >= month_after_end_date:
                        break

                    if date_temp > self.end_date:
                        continue

                    if date_temp < self.start_date:
                        return

                    raw_edition = day.css('a[data-toggle="modal-pdf"]::text').get()
                    extra = "extra" in raw_edition.lower()

                    edition = re.sub(r"\D", "", raw_edition)

                    url_pdf = day.css('a[data-toggle="modal-pdf"]::attr(href)').get()

                    yield Gazette(
                        date=date_temp,
                        edition_number=edition,
                        is_extra_edition=extra,
                        file_urls=[url_pdf],
                        power="executive",
                    )
