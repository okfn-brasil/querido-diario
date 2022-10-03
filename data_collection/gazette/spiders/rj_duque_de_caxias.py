import dateparser
import datetime as dt

from scrapy import Request
from scrapy import Selector

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RjDuqueDeCaxiasSpider(BaseGazetteSpider):
    TERRITORY_ID = "3301702"

    GAZETTE_ELEMENT_CSS = "ul.jornal li"
    NEXT_PAGE_CSS = "ul.pagination li.next a::attr(href)"
    DATE_CSS = "span.article-date::text"
    EXTRA_EDITION_CSS = "span.edicao_extraordinaria::text"
    DATE_REGEX = r"([\d]+)[ |]+([\w]+)[ |]+([\d]+)"

    allowed_domains = ["duquedecaxias.rj.gov.br"]
    name = "rj_duque_de_caxias"
    DUQUE_DE_CAXIAS_START_URL = "http://duquedecaxias.rj.gov.br/portal/boletim-oficial.html"
    PDF_URL = "http://duquedecaxias.rj.gov.br/portal/{}"
    PHASE2_YEAR_URL = "https://duquedecaxias.rj.gov.br/portal/{}.html"  # 2017 to (actual_year-1)

    def start_requests(self):
        # Actual year
        actual_year = dt.datetime.today().year
        january_first_actual_year = dt.date(actual_year, 1, 1)
        if self.end_date >= january_first_actual_year:
            yield Request(self.DUQUE_DE_CAXIAS_START_URL)

        # Phase 2 (2017 to actual_year - 1)
        start_date_year = self.start_date.year
        if start_date_year < 2017:
            start_date_year = 2017
        end_date_year = self.end_date.year
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

        # TODO: Criar dois tipos de parsers para o período de 2017 a ano_atual - 1 e anterior a 2017 (2013 a 2016)

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

    def parse_phase2(self, response):
        """
        @scrapes date file_urls is_extra_edition power
        """
        month_header_cells = 3

        for month_div_no in range(2, 14):
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

    def extract_url(self, element):
        path = element.css("a::attr(href)").extract_first()
        return self.PDF_URL.format(path)

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
