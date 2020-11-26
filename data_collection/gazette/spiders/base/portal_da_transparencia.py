import datetime
import re

import dateparser
from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class PortalDaTransparenciaBaseSpider(BaseGazetteSpider):
    allowed_domains = ["portaldatransparencia.com.br"]
    start_date = datetime.date(2000, 1, 1)

    def parse(self, response):
        EDITION_QUERY = "div.box-edicao"
        for issue in response.css(EDITION_QUERY):
            date = self.get_issue_date(issue)
            if date < self.start_date:
                return

            gazette_file_url = self.get_issue_file_url(response, issue)

            edition_number, is_extra_edition = self.get_edition_number(issue)

            yield Gazette(
                date=date,
                file_urls=[gazette_file_url],
                is_extra_edition=is_extra_edition,
                edition_number=edition_number,
                power="executive",
            )

        next_page_url = response.urljoin(response.css("a.proximo::attr(href)").get())
        if next_page_url:
            yield Request(next_page_url)

    def get_issue_date(self, issue):
        DATE_QUERY = "div.data-caderno ::text"
        issue_date = issue.css(DATE_QUERY).get()
        return dateparser.parse(issue_date, languages=["pt"]).date()

    def get_issue_file_url(self, response, issue):
        DOWNLOAD_QUERY = "a.btn_visualizar::attr(href)"
        return response.urljoin(issue.css(DOWNLOAD_QUERY).get())

    def get_edition_number(self, issue):
        EDITION_NUMBER_QUERY = "span.edicao > strong ::text"

        edition_text, issue_number = issue.css(EDITION_NUMBER_QUERY).get().split("|")

        edition_number = int(re.sub("[^0-9]", "", edition_text))
        is_extra_edition = "Caderno 1" not in issue_number
        return edition_number, is_extra_edition
