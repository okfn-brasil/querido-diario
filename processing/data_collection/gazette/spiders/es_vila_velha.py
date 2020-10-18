import dateparser

from datetime import datetime, date
from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider
from scrapy import FormRequest, Request
import os


class VilaVelhaSpider(BaseGazetteSpider):
    name = "es_vila_velha"
    allowed_domains = ["www.vilavelha.es.gov.br"]

    TERRITORY_ID = "3205200"
    GAZETTE_URL_CSS = "td:last-child a::attr(href)"
    GAZETTE_DATE_CSS = "td:nth-child(2) span b::text"
    GAZETTE_ISSUE_CSS = "td:nth-child(3) span b::text"
    JAVASCRIPT_POSTBACK_REGEX = r"javascript:__doPostBack\('(.*)',''\)"

    # this is the first date which has gazettes available (edition number 1)
    start_date = date(2016, 7, 1)

    def start_requests(self):
        date_param = self.start_date.strftime("%d/%m/%Y")
        base_url = "https://www.vilavelha.es.gov.br/diariooficial/ConsultaDiario.aspx"
        gazettes_url = f"{base_url}?dataInicial={date_param}"
        yield Request(gazettes_url)

    def parse(self, response):
        for element in response.css("#ctl00_cpConteudo_gvDocumentos tr"):
            if element.css("th").extract():
                continue

            date = element.css(self.GAZETTE_DATE_CSS).extract_first()
            date = dateparser.parse(date, languages=["pt"]).date()
            url = element.css(self.GAZETTE_URL_CSS)
            gazette_issue = element.css(self.GAZETTE_ISSUE_CSS).extract_first()
            is_extra = "EXTRA" in gazette_issue
            edition_number = gazette_issue.split(" ")[0]
            event_target = url.re(self.JAVASCRIPT_POSTBACK_REGEX).pop()

            gazette = Gazette(
                date=date,
                edition_number=edition_number,
                is_extra_edition=is_extra,
                territory_id=self.TERRITORY_ID,
                power="executive_legislature",
                scraped_at=datetime.utcnow(),
            )

            yield FormRequest.from_response(
                response,
                formdata={"__EVENTARGUMENT": "", "__EVENTTARGET": event_target},
                dont_click=True,
                dont_filter=True,
                method="POST",
                meta={"item": gazette},
                callback=self._save_pdf,
            )

    def _save_pdf(self, response):
        gazette = response.meta["item"]
        filename = f"es_vila_velha_{gazette['date']}.pdf"
        path = os.path.join("/mnt/data/full", filename)
        with open(path, "wb") as f:
            f.write(response.body)

        yield gazette
