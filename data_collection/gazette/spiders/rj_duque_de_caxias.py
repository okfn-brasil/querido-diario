from datetime import date, datetime

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RjDuqueDeCaxiasSpider(BaseGazetteSpider):
    TERRITORY_ID = "3301702"
    name = "rj_duque_de_caxias"
    allowed_domains = ["duquedecaxias.rj.gov.br"]
    base_url_before_2017 = (
        "https://duquedecaxias.rj.gov.br/portal/boletim-oficial/{}/{}"
    )
    base_url_after_2017 = "https://duquedecaxias.rj.gov.br/portal/{}.html"
    base_url_2021 = "https://duquedecaxias.rj.gov.br/portal/boletim-oficial.html"
    start_date = date(2013, 1, 1)

    month_names = [
        "Janeiro",
        "Fevereiro",
        "Marco",
        "Abril",
        "Maio",
        "Junho",
        "Julho",
        "Agosto",
        "Setembro",
        "Outubro",
        "Novembro",
        "Dezembro",
    ]

    def start_requests(self):
        year = self.start_date.year
        if year > 2016:
            if year == 2021:
                url = self.base_url_2021
            else:
                url = self.base_url_after_2017.format(year)
            yield scrapy.Request(url)
        else:
            while year < 2017:
                month = self.start_date.month
                while month < len(self.month_names):
                    url = self.base_url_before_2017.format(
                        year, "{:02d}".format(month + 1) + "-" + self.month_names[month]
                    )
                    day = 1
                    yield scrapy.Request(
                        url,
                        callback=self.parse,
                        cb_kwargs={"day": day, "month": month + 1, "year": year},
                    )
                    month += 1
                year += 1

    def parse(self, response, day, month, year):
        if response.status == 200:
            for element in response.xpath('//a[contains(@href,"pdf")]/@href'):
                file_name = element.get()

                gazette_date = datetime.strptime(
                    f"{year}-{month}-{day}", "%Y-%m-%d"
                ).date()

                if ".html" in response.url:
                    url = self.base_url + element.get()
                else:
                    url = response.url + element.get()

                extra_edition = "extra" in element.get().lower()

                if extra_edition or file_name.lower() in "especial":
                    gazette_edition_number = (
                        file_name.lower().replace(".pdf", "").replace("boletim_")
                    )
                else:
                    edition_number = []
                    if file_name.find("-") > 0:
                        edition_number = file_name.split("-")
                    else:
                        edition_number = file_name.split("_")
                    for e in edition_number:
                        if e.isnumeric() and int(e.isnumeric()) > 6006:
                            gazette_edition_number = e
                        elif e.lower() in "vol" or e.lower()[0] == "v":
                            gazette_edition_number = gazette_edition_number + "-" + e

                yield Gazette(
                    date=gazette_date,
                    file_urls=[url],
                    is_extra_edition=extra_edition,
                    edition_number=edition_number,
                    power="executive_legislative",
                )
