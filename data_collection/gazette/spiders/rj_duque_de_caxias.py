import dateparser
import datetime as dt
import calendar
import pandas as pd
import locale
import re

from scrapy import Request
from scrapy import Selector

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RjDuqueDeCaxiasSpider(BaseGazetteSpider):
    TERRITORY_ID = "3301702"
    start_date = dt.date(2013, 1, 2)
    allowed_domains = ["duquedecaxias.rj.gov.br"]
    name = "rj_duque_de_caxias"
    DUQUE_DE_CAXIAS_START_URL = "http://duquedecaxias.rj.gov.br/portal/boletim-oficial.html"
    PDF_URL = "http://duquedecaxias.rj.gov.br/portal/{}"
    PHASE2_YEAR_URL = "https://duquedecaxias.rj.gov.br/portal/{}.html"  # 2017 to (actual_year-1)
    PHASE2_START_YEAR = 2017
    PHASE1_YEAR_URL = "https://duquedecaxias.rj.gov.br/portal/boletim-oficial/{}"
    PHASE1_START_YEAR = 2013
    PHASE1_END_YEAR = 2016

    def start_requests(self):
        # Actual year
        actual_year = dt.datetime.today().year
        january_first_actual_year = dt.date(actual_year, 1, 1)
        if self.end_date >= january_first_actual_year:
            yield Request(self.DUQUE_DE_CAXIAS_START_URL)
        locale.setlocale(locale.LC_TIME, "pt_BR")  # Get month name as needed... (2013/01-Janeiro)

        # Phase 1 (2013 to 2016)
        # https://duquedecaxias.rj.gov.br/portal/boletim-oficial/2013/01-Janeiro/
        if self.start_date.year <= self.PHASE1_END_YEAR:
            if self.end_date.year > self.PHASE1_END_YEAR:
                phase1_end_date = dt.date(self.PHASE1_END_YEAR, 12, 31)
            else:
                phase1_end_date = dt.datetime(self.end_date.year, self.end_date.month,
                                              calendar.monthrange(self.end_date.year, self.end_date.month)[1])
            self.logger.debug("start_date: %s phase1_end_date: %s", self.start_date.strftime("%d/%m/%Y"),
                              phase1_end_date.strftime("%d/%m/%Y"))
            month_list = pd.date_range(self.start_date, phase1_end_date, freq='M').strftime("%Y/%m-%B").tolist()
            self.logger.debug("month_list: %s", month_list)
            for month in month_list:
                url_phase1 = self.PHASE1_YEAR_URL.format(month).replace('ç', 'c')  # Março -> Marco
                self.logger.debug("url phase1: %s", url_phase1)
                yield Request(url_phase1, callback=self.parse_phase1)

        # Phase 2 (2017 to actual_year - 1)
        # https://duquedecaxias.rj.gov.br/portal/2017.html
        start_date_year = self.start_date.year
        end_date_year = self.end_date.year
        if start_date_year < 2017:
            start_date_year = 2017
        if end_date_year == actual_year:
            end_date_year = actual_year - 1

        self.logger.debug("start_date_year: %d, end_date_year: %d, actual_year: %d", start_date_year, end_date_year,
                          actual_year)
        if start_date_year < actual_year and end_date_year >= 2017:
            for year in range(start_date_year, end_date_year + 1):
                yield Request(self.PHASE2_YEAR_URL.format(year), callback=self.parse_phase2)

    def parse(self, response):
        """
        @url http://duquedecaxias.rj.gov.br/portal/boletim-oficial.html
        @returns requests 1
        @scrapes date file_urls is_extra_edition power
        """

        for element in response.xpath('//div[contains(@class,"panel-body")]').getall():
            self.logger.debug(element)
            pdf_marker = Selector(text=element).xpath('//i[contains(@class,"far fa-file-pdf")]').get()
            if pdf_marker is not None:
                raw_edition_number = Selector(text=element).xpath('string(//div//div[1])').get()
                raw_date = Selector(text=element).xpath('string(//div//div[2])').get()
                date = dateparser.parse(raw_date, languages=["pt"]).date()
                url = self.extract_url(Selector(text=element))
                is_extra_edition, edition_number = self.extract_edition_info(raw_edition_number)

                self.logger.debug("%s, %s, %s, %s, %s, %s", raw_edition_number, raw_date, date.strftime('%d/%m/%Y'),
                                  url, is_extra_edition, edition_number)

                if self.start_date <= date <= self.end_date:
                    yield Gazette(
                        date=date,
                        file_urls=[url],
                        is_extra_edition=is_extra_edition,
                        edition_number=edition_number,
                        power="executive_legislative",
                    )

    def parse_phase1(self, response):
        """
        @scrapes date file_urls is_extra_edition power
        """
        year_month_pattern = r'\d{4}/\d{2}'
        day_pattern = r'-\d{2}'

        for link in response.css("a::attr(href)").getall():
            if not link.startswith(("?", "/")):
                gazzete_url = response.request.url + link
                gazzete_date = dt.datetime.strptime(re.findall(year_month_pattern, gazzete_url)[0] +
                                           re.findall(day_pattern, gazzete_url)[0],
                                           "%Y/%m-%d").date()
                gazzete_is_extra_edition, gazzete_edition_number = self.extract_edition_info_phase2(link)

                self.logger.debug("%s, %s, %s, %s", gazzete_date, link, gazzete_is_extra_edition, gazzete_edition_number)

                if self.start_date <= gazzete_date <= self.end_date:
                    yield Gazette(
                        date=gazzete_date,
                        file_urls=[gazzete_url],
                        is_extra_edition=gazzete_is_extra_edition,
                        edition_number=gazzete_edition_number,
                        power="executive_legislative",
                    )

    def parse_phase2(self, response):
        """
        @scrapes date file_urls is_extra_edition power
        """
        month_header_cells = 3

        for month_div_no in range(1, 14):
            for month in response.xpath('/html/body/center/div[{}]'.format(month_div_no)).getall():
                path_list = Selector(text=month).css("a::attr(href)").getall()
                raw_month_text_cells = Selector(text=month).xpath("//div//text()").getall()
                month_text_cells = []
                for cell in raw_month_text_cells:
                    if "\n" not in cell:
                        month_text_cells.append(cell)
                gazzete_qt = (len(month_text_cells) - month_header_cells) // 2
                for gazzete_index in range(gazzete_qt - 1):
                    raw_edition_number = month_text_cells[month_header_cells + gazzete_index*2]
                    raw_date = month_text_cells[month_header_cells + gazzete_index*2+1]
                    date = dateparser.parse(raw_date, languages=["pt"]).date()
                    url = self.PDF_URL.format(path_list[gazzete_index])
                    is_extra_edition, edition_number = self.extract_edition_info(raw_edition_number)

                    self.logger.debug("%s, %s, %s, %s, %s, %s", raw_edition_number, raw_date, date.strftime('%d/%m/%Y'),
                                      url, is_extra_edition, edition_number)

                    if self.start_date <= date <= self.end_date:
                        yield Gazette(
                            date=date,
                            file_urls=[url],
                            is_extra_edition=is_extra_edition,
                            edition_number=edition_number,
                            power="executive_legislative",
                        )

    def extract_edition_info(self, raw_edition_info):
        self.logger.debug("%s, %s", raw_edition_info, raw_edition_info.split())
        is_extra_edition = False
        if "EXTRA" in raw_edition_info.upper() or "ESPECIAL" in raw_edition_info.upper():
            # Boletim Extraordinário 02 / Boletim Especial 001 / Boletim Extraordinário
            is_extra_edition = True
            if len(raw_edition_info.split()) > 2:
                edition_number = raw_edition_info.split()[2]
            else:
                edition_number = ""
        elif "VOL" in raw_edition_info.upper():
            is_extra_edition = True
            edition_number = raw_edition_info.split()[1]  # Boletim 7086 vol2 / Boletim 6400 Vol.1
        else:
            edition_number = raw_edition_info.split()[1]  # Boletim 6393
        return is_extra_edition, edition_number

    def extract_edition_info_phase2(self, raw_edition_info):
        """
        Since the number of exceptions from 2013 to 2016 are small these exceptions are mapped in a dictionary
        """
        self.logger.debug("%s, %s", raw_edition_info, raw_edition_info.split())
        is_extra_edition = False

        # If raw_edition_info doesn't match the regex then it's an extra edition
        try:
            edition_pattern = r'\d{4}-'
            edition_number = re.findall(edition_pattern, raw_edition_info)[0][:4]
        except IndexError:
            is_extra_edition = True
            exception_dict = {'01E-25.pdf': '01', '6211A-05.pdf': '6211', '6186_2-27.pdf': '6186',
                              '6140_2-10.pdf': '6140', 'E02-25.pdf': '02', '6292_2-29.pdf': '6292'}
            edition_number = exception_dict[raw_edition_info]
        return is_extra_edition, edition_number

