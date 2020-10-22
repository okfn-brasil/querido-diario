from datetime import date

import dateparser
from scrapy import FormRequest, Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class VilaVelhaSpider(BaseGazetteSpider):
    name = "es_vila_velha"
    allowed_domains = ["www.vilavelha.es.gov.br"]

    TERRITORY_ID = "3205200"
    GAZETTE_URL_CSS = "td:last-child a::attr(href)"
    GAZETTE_DATE_CSS = "td:nth-child(2) span b::text"
    GAZETTE_ISSUE_CSS = "td:nth-child(3) span b::text"
    JAVASCRIPT_POSTBACK_REGEX = r"javascript:__doPostBack\('(.*)',''\)"

    start_date = date(2016, 7, 1)

    def start_requests(self):
        date_param = self.start_date.strftime("%d/%m/%Y")
        base_url = "https://www.vilavelha.es.gov.br/diariooficial/ConsultaDiario.aspx"
        gazettes_url = f"{base_url}?dataInicial={date_param}"
        yield Request(gazettes_url)

    def parse(self, response):
        for element in response.css("#ctl00_cpConteudo_gvDocumentos tr"):
            is_header = element.css("th").extract() != []
            if is_header:
            	continue

            date = element.css(self.GAZETTE_DATE_CSS).extract_first()
            date = dateparser.parse(date, languages=["pt"]).date()
            event_target = element.css(self.GAZETTE_URL_CSS).re_first(
                self.JAVASCRIPT_POSTBACK_REGEX
            )
            gazette_issue = element.css(self.GAZETTE_ISSUE_CSS).extract_first()
            is_extra = "EXTRA" in gazette_issue
            edition_number = gazette_issue.split(" ")[0]

            document_request = FormRequest.from_response(
                response, formdata={"__EVENTTARGET": event_target}, method="POST"
            )

            yield Gazette(
                date=date,
                file_requests=[document_request],
                edition_number=edition_number,
                is_extra_edition=is_extra,
                power="executive_legislative",
            )
