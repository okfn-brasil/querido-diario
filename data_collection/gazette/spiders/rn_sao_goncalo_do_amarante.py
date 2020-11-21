import datetime
import re

import dateparser
import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class SpSaoGoncaloDoAmarante(BaseGazetteSpider):
    """
    São Gonçalo do Amarante has a primary url with
    recent gazettes (https://saogoncalo.rn.gov.br/diario-oficial/)
    and another with old gazettes (https://saogoncalo.rn.gov.br/jornal-oficial/).
    The transition date of the urls occurred on 22/03/2017.
    The gazettes available in the old url can be obtained by directly accessing the page of the year.
    """

    TERRITORY_ID = "2412005"
    name = "rn_sao_goncalo_do_amarante"
    allowed_domains = ["saogoncalo.rn.gov.br"]

    start_date = datetime.date(2013, 1, 2)
    transition_date = datetime.date(2017, 3, 22)

    NEW_URL = "https://saogoncalo.rn.gov.br/diario-oficial/"
    OLD_URL = "https://saogoncalo.rn.gov.br/jom-{year}/"
    PDF_URL = (
        "https://saogoncalo.rn.gov.br/wp-content/uploads/{year}/{month}/{name}.pdf"
    )

    def start_requests(self):
        """
        Yields a request for the new page and a request for each year from the start date to the transition date
        """
        yield scrapy.Request(self.NEW_URL, callback=self.parse_page_after_transition)

        if self.start_date < self.transition_date:
            for year in list(
                range(self.start_date.year, self.transition_date.year + 1)
            ):
                yield scrapy.Request(
                    self.OLD_URL.format(year=year),
                    callback=self.parse_page_before_transition,
                )

    def parse_page_after_transition(self, response):
        document_list = response.css(".post-attachment")

        for document in document_list:
            yield self.get_gazette(document=document, is_after_transition=True)

    def parse_page_before_transition(self, response):
        document_list = response.css(".inner a")

        for document in document_list:
            yield self.get_gazette(document=document, is_after_transition=False)

    def get_file_url(self, title, date):
        name = re.sub("[ -]+", "-", title)
        month = str(date.month).zfill(2)
        year = date.year
        return self.PDF_URL.format(year=year, month=month, name=name)

    def get_gazette(self, document, is_after_transition):
        """
        Extract the information from the document and return a Gazette item
        """
        title = document.css("::text").get()

        edition_number = re.search(r"\d+", title).group(0)
        is_extra_edition = bool(re.search(r"EXTRA", title, re.IGNORECASE))

        date_text = re.search(
            r"(\d{1,2}\w+\d{4})|(\d{1,2}.\d{1,2}.\d{4})", title
        ).group(0)
        date = dateparser.parse(date_text, languages=["pt"]).date()

        if is_after_transition:
            file_url = self.get_file_url(title, date)
        else:
            file_url = document.css("::attr(href)").get()

        return Gazette(
            date=date,
            edition_number=edition_number,
            file_urls=[file_url],
            power="executive_legislative",
            is_extra_edition=is_extra_edition,
        )
