import re
from datetime import date, datetime
import json

import dateparser
from dateutil.rrule import MONTHLY, rrule
import scrapy
from scrapy.http import JsonRequest

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RnParnamirimSpider(BaseGazetteSpider):
    """
    Parnamirim has a primary url with recent gazettes (http://diariooficial.parnamirim.rn.gov.br/)
    and another with old gazettes (https://www.parnamirim.rn.gov.br/diarioOficial.jsp).
    The transition date of the urls occurred on 17/07/2018.
    The gazettes available in the old url can be obtained by directly accessing the page.
    """

    name = "rn_parnamirim"
    allowed_domains = ["diariooficial.parnamirim.rn.gov.br", "www.parnamirim.rn.gov.br"]
    TERRITORY_ID = "2403251"
    start_date = date(2009, 1, 13)
    transition_date = date(2018, 7, 17)
    NEW_URL = ("http://sgidom.parnamirim.rn.gov.br/rest/sgidiario_diario_service/diarios_por_mes?data={year}-{month:02d}")
    OLD_URL = "https://www.parnamirim.rn.gov.br/diarioOficial.jsp"

    custom_settings = {
        "DOWNLOAD_DELAY": 2,
    }

    def start_requests(self):
        if self.start_date < self.transition_date:
            yield scrapy.Request(self.OLD_URL, callback=self.parse_page_before_transition)

        if self.end_date > self.transition_date:
            initial_date = date(self.start_date.year, self.start_date.month, 1)
            interval = rrule(freq=MONTHLY, dtstart=initial_date, until=self.end_date)

            for item in interval:
                url = self.NEW_URL.format(year=item.year, month=item.month)
                yield JsonRequest(url, callback=self.parse_json_after_transition)

    def parse_json_after_transition(self, response):
        json_response = json.loads(response.body.decode('utf-8'))

        for gazette in json_response:
            id = gazette['id']
            edition_number = gazette['numero']
            publication_date = datetime.fromtimestamp(gazette['data_publicacao'] / 1000.0).date()
            is_extra_edition = bool(re.search(r"Especial", edition_number, re.IGNORECASE))
            # The id queryParam, it's not used for API. But Parnamirim has many gazettes at same date,
            # not marked as Extra Edition. The QueridoDiarioFilesPipeline#file_path creates a hashname 
            # to a PDF file based in the document URL, so when there are more than one gazette in same
            # date, it was ovewriting the PDF, because the URL is the same for all.
            document_request = JsonRequest(
                url=f"http://diariooficial.parnamirim.rn.gov.br:8400/export?id={id}",
                data={
                    "domQueryParams": f"publicar=false&id_diario={id}",
                    "domDataCabecalho": publication_date.strftime("%d/%m/%Y"),
                    "domOrigin": "http://sgidom.parnamirim.rn.gov.br",
                    "diarioId": id
                }
            )

            yield Gazette(
                date=publication_date,
                edition_number=edition_number,
                file_requests=[document_request],
                power="executive_legislative",
                is_extra_edition=is_extra_edition,
            )

    def parse_page_before_transition(self, response):
        document_list = response.css("div.sub-dropdown > ul > ul > li")

        for document in document_list:
            yield self.get_gazette(document=document)

    def get_edition_number(self, edition_text):
        pattern_1 = re.compile(r"^[A-Z ]+[ -]+[n].[ ]*(\d+)", re.IGNORECASE)
        pattern_2 = re.compile(r"^[A-Z ]+[ ]*(\d+)", re.IGNORECASE)

        if pattern_1.match(edition_text):
            return pattern_1.match(edition_text).group(1)
        elif pattern_2.match(edition_text):
            return pattern_2.match(edition_text).group(1)

        self.logger.warning(f"Unable to retrieve EDITION number for {edition_text}.")

        return None

    def get_gazette(self, document):
        """
        Extract the information from the document and return a Gazette item
        """

        date_text = document.css("span::text").get()
        edition_text = document.css("a::text").get()
        edition_number = self.get_edition_number(edition_text)

        is_extra_edition = bool(re.search(r"Especial", edition_text, re.IGNORECASE))
        publication_date = dateparser.parse(date_text, date_formats=['%d de %B de %Y']).date()
        file_url = f"https://www.parnamirim.rn.gov.br/{document.css('a::attr(href)').get()}"

        return Gazette(
            date=publication_date,
            edition_number=edition_number,
            file_urls=[file_url],
            power="executive_legislative",
            is_extra_edition=is_extra_edition,
        )
