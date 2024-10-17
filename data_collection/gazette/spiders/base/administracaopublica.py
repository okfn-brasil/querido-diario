import re
from datetime import datetime
from typing import Any

from dateutil.rrule import DAILY, rrule
from scrapy import Request
from scrapy.http import Response

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class BaseAdministracaoPublicaSpider(BaseGazetteSpider):
    """
    Base spider for cities using the https://administracaopublica.com.br/diario-oficial?token= plataform.
    Gazzetes are also avaiable in http://www.transparenciadministrativa.com.br/diario/diariov2.xhtml?token=.
    """

    token: str
    allowed_domains = ["administracaopublica.com.br"]

    def start_requests(self):
        dates = list(
            rrule(freq=DAILY, interval=20, dtstart=self.start_date, until=self.end_date)
        )
        dates.append(self.end_date)

        for i in range(len(dates) - 1):
            de = dates[i].strftime("%Y-%m-%d")
            ate = dates[i + 1].strftime("%Y-%m-%d")
            yield Request(
                f"https://administracaopublica.com.br/diario-oficial?token={self.token}&de={de}&ate={ate}"
            )

    def parse(self, response: Response, **kwargs: Any) -> Any:
        gazettes = response.css(".diario_item_diario__g9Qfw")
        for gazzete in gazettes:
            href = gazzete.css('[class*="generics_button_baixar__"]::attr(href)').get()
            if href is None:
                continue
            pattern = gazzete.css("::text").extract()
            match pattern:
                case [edition, power, date, _]:
                    pass
                case [edition, date, _]:
                    power = ""
            power_dict = {
                "EXECUTIVO": "executive",
                "LEGISLATIVO": "legislative",
            }
            yield Gazette(
                edition_number=re.findall(r"\s*(\d+\/\d+)\s*", edition),
                date=datetime.strptime(date, "%d/%m/%Y").date(),
                file_urls=[f"https://administracaopublica.com.br{href}"],
                is_extra_edition=power == "EXTRA",
                power=power_dict.get(power, "executive_legislative"),
            )
