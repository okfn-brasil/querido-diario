import re
from datetime import datetime as dt

from dateutil.rrule import DAILY, rrule
from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class BaseAdministracaoPublicaSpider(BaseGazetteSpider):
    """
    Base spider for cities using the https://administracaopublica.com.br/diario-oficial?token= plataform.
    Gazettes are also available in http://www.transparenciadministrativa.com.br/diario/diariov2.xhtml?token=.
    """

    allowed_domains = ["administracaopublica.com.br"]

    def start_requests(self):
        dates = list(
            rrule(freq=DAILY, interval=7, dtstart=self.start_date, until=self.end_date)
        )
        dt_end_date = dt(self.end_date.year, self.end_date.month, self.end_date.day)
        if dt_end_date not in dates:
            dates.append(dt_end_date)

        for i in range(len(dates) - 1):
            start = dates[i].strftime("%Y-%m-%d")
            end = dates[i + 1].strftime("%Y-%m-%d")
            yield Request(
                f"https://www.administracaopublica.com.br/diario-oficial?token={self.token}&de={start}&ate={end}"
            )

    def parse(self, response):
        gazettes = response.css('[class*="diario_item_diario__"]')
        for gazette in gazettes:
            if "Nenhum resultado encontrado" not in response.text:
                href = gazette.css(
                    '[class*="generics_button_baixar__"]::attr(href)'
                ).get()
                pattern = gazette.css("::text").getall()

                match pattern:
                    case [edition, _, power, date, _]:
                        pass
                    case [edition, _, date, _]:
                        power = ""
                power_dict = {
                    "EXECUTIVO": "executive",
                    "LEGISLATIVO": "legislative",
                }
                yield Gazette(
                    edition_number=re.search(r"(\d+)[-/]", edition).group(1),
                    date=dt.strptime(date, "%d/%m/%Y").date(),
                    file_urls=[f"https://www.administracaopublica.com.br{href}"],
                    is_extra_edition=power == "EXTRA",
                    power=power_dict.get(power, "executive_legislative"),
                )
