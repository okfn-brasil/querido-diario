import re
from datetime import date, datetime

import scrapy
from dateparser import parse

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RjDuqueDeCaxiasSpider(BaseGazetteSpider):
    TERRITORY_ID = "3301702"
    name = "rj_duque_de_caxias"
    allowed_domains = ["duquedecaxias.rj.gov.br"]
    portal_url = "https://duquedecaxias.rj.gov.br/portal/{}.html"
    directory_url = "https://duquedecaxias.rj.gov.br/portal/boletim-oficial/{}/{}"

    months = [
        "01-Janeiro",
        "02-Fevereiro",
        "03-Marco",
        "04-Abril",
        "05-Maio",
        "06-Junho",
        "07-Julho",
        "08-Agosto",
        "09-Setembro",
        "10-Outubro",
        "11-Novembro",
        "12-Dezembro",
    ]

    def start_requests(self):
        urls = [
            {
                "url": "https://duquedecaxias.rj.gov.br/portal/boletim-oficial.html",
                "year": date.today().year,
                "month": 1,
            }
        ]

        for year in range(2013, 2017):
            for month in self.months:
                urls.append(
                    {
                        "url": self.directory_url.format(year, month),
                        "year": year,
                        "month": month[:2],
                    }
                )

        for year in range(2017, date.today().year):
            urls.append(
                {
                    "url": self.portal_url.format(year),
                    "year": year,
                    "month": None,
                }
            )

        for url in urls:
            yield scrapy.Request(
                url["url"],
                callback=self.parse,
                cb_kwargs={"year": url["year"], "month": url["month"]},
            )

    def parse(self, response, year, month):
        if response.status == 200:
            for element in response.xpath('//a[contains(@href,"pdf")]/@href'):
                url = response.urljoin(element.get())

                name = element.get().lower()

                gazette_date = self.handle_date(response, element.get(), year, month)

                extra_edition = self.is_extra_edition(year, name)

                edition_number = self.handle_edition_number(
                    response, element.get(), year
                )

                yield Gazette(
                    date=gazette_date,
                    file_urls=[url],
                    is_extra_edition=extra_edition,
                    edition_number=edition_number,
                    territory_id=self.TERRITORY_ID,
                    power="executive_legislative",
                )

    def is_extra_edition(self, year, name):
        if year <= 2016:
            extras = ["e", "a"]
            return bool([ele for ele in extras if (ele in name)])
        else:
            extras = ["vol", "especial", "extra"]
            return bool([ele for ele in extras if (ele in name)])

    def handle_date(self, response, search_for, year, month):
        gazette_date = None
        if year <= 2016:
            day = re.search(r"\-(.*?)\.", search_for.lower()).group(1)
            gazette_date = datetime.strptime(f"{year}-{month}-{day}", "%Y-%m-%d").date()
        else:
            unparsed_date = response.xpath(
                f'//div//a[contains(@href,"{search_for}")]/../preceding-sibling::div[1]'
            ).re(r"(\d{1,2}\s+de\s+\w+\s+\d{4})")[0]
            gazette_date = parse(unparsed_date, languages=["pt"]).date()

        return gazette_date

    def handle_edition_number(self, response, search_for, year):
        edition_number = "1"
        if year <= 2016:
            unparsed_edition = re.search(r"\_(.*?)\-", search_for.lower())
            if unparsed_edition:
                edition_number = unparsed_edition.group(1)
        else:
            unparsed_edition = response.xpath(
                f'//div//a[contains(@href,"{search_for}")]/../preceding-sibling::div[2]'
            ).re(r"(([vV]ol|IO)(.*?)\d+)")
            if unparsed_edition:
                edition_number = unparsed_edition[0].lower().replace("vol", "")
                edition_number = edition_number.replace(".", "").replace(" ", "")
                edition_number = edition_number.replace("io", "")

        return edition_number
