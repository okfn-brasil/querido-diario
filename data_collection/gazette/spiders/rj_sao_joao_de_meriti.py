import datetime
import json
import re

import scrapy
from dateutil.rrule import MONTHLY, rrule

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class SpSaoJoaoDeMeritiSpider(BaseGazetteSpider):
    TERRITORY_ID = "3305109"
    name = "rj_sao_joao_de_meriti"
    allowed_domains = ["meriti.rj.gov.br"]

    URL_BEFORE_2018 = "https://meriti.rj.gov.br/dom_mp/"
    URL_FROM_2018 = (
        "https://transparencia.meriti.rj.gov.br/diario_oficial_get.php?mesano="
    )

    start_date = datetime.date(2011, 9, 30)
    end_date = datetime.date.today()

    def start_requests(self):
        janeiro_2018 = datetime.date(2018, 1, 1)
        for month in self.months_interval():
            if month < janeiro_2018:
                yield scrapy.Request(
                    f"{self.URL_BEFORE_2018}{month.year}{month.month:02}.php",
                    callback = self.parse_month_before_2018
                )
            else:
                yield scrapy.Request(
                    f"{self.URL_FROM_2018}{month.month}/{month.year}",
                    callback = self.parse_month_from_2018
                )

    def months_interval(self):
        month_rule = rrule(freq=MONTHLY, dtstart=self.start_date, until=self.end_date)
        months = [month.date() for month in month_rule]
        if months and months[-1].month != self.end_date.month:
            months.append(self.end_date)
        return months

    def get_day_fom_pdf_link(self, pdf_link):
        day_regex = r"[/-](\d{1,2})[^\d/][^/]*.pdf"
        day = int(re.search(day_regex, pdf_link, re.IGNORECASE).group(1))
        return day

    def parse_gazette_before_2018(self, month_response, pdf_link):
        year = int(month_response.url[-10:-6])
        month = int(month_response.url[-6:-4])
        day = self.get_day_fom_pdf_link(pdf_link)
        date = datetime.date(year, month, day)

        return Gazette(
            date=date,
            file_urls=[pdf_link],
            is_extra_edition=False,
            power="executive_legislative",
        )

    def get_pdf_links(self, month_response):
        upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        lower = "abcdefghijklmnopqrstuvwxyz"
        pdf_links = month_response.xpath(
            f"//a[contains(translate(@href, {upper}, {lower}), '.pdf')]//@href"
        ).getall()

        return pdf_links

    def parse_month_before_2018(self, response):
        gazettes = []

        for pdf_link in self.get_pdf_links(response):
            gazette = self.parse_gazette_before_2018(response, pdf_link)
            if self.start_date <= gazette["date"] <= self.end_date:
                gazettes.append(gazette)

        return gazettes

    def parse_gazette_from_2018(self, gazette_entry):
        edition_number = int(re.search(r"\d+", gazette_entry["ANEXO"]).group())
        is_extra_edition = "EXTRA" in gazette_entry["ANEXO"]
        date = datetime.datetime.strptime(
            gazette_entry["Data_Formatada"], "%d/%m/%Y"
        ).date()
        base_link = "https://transparencia.meriti.rj.gov.br/webrun/WEB-ObterAnexo.rule?sys=LAI&codigo="
        pdf_link = base_link + f"{gazette_entry['Codigo_ANEXO']}"

        return Gazette(
            date=date,
            edition_number=edition_number,
            is_extra_edition=is_extra_edition,
            file_urls=[pdf_link],
            power="executive_legislative",
        )

    def parse_month_from_2018(self, response):
        gazettes = []
        month_entries = json.loads(response.text)

        for gazette_entry in month_entries:
            gazette = self.parse_gazette_from_2018(gazette_entry)
            if self.start_date <= gazette["date"] <= self.end_date:
                gazettes.append(gazette)

        return gazettes
