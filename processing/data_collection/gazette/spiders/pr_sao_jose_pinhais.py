import re
import dateparser
import w3lib.url
from urllib.parse import urlencode

from datetime import datetime, date
from scrapy import Request
from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class PrSaoJosePinhaisSpider(BaseGazetteSpider):
    TERRITORY_ID = "4125506"
    allowed_domains = ["diariooficial.sjp.pr.gov.br"]
    name = "pr_sao_jose_pinhais"

    BASE_URL = "http://diariooficial.sjp.pr.gov.br/"
    GAZETTE_ELEMENT_CSS = ".container-publicacao .item-publicacao"
    DATE_XPATH = './/div[contains(@class, "item-label") and text()="Publicado em"]/following-sibling::div[1]/text()'
    LAST_PAGE_CSS = ".item-paginacao a:last-child::attr(href)"

    def start_requests(self):
        params = {"entidade": 12526, "pg": 1}

        if hasattr(self, "start_date"):
            params.update(
                {
                    "dt_publicacao_de": self.start_date.strftime("%d/%m/%Y"),
                    "dt_publicacao_ate": date.today().strftime("%d/%m/%Y"),
                }
            )

        yield Request(f"{self.BASE_URL}?{urlencode(params)}")

    def parse(self, response):
        for element in response.css(self.GAZETTE_ELEMENT_CSS):
            url = element.css("a::attr(href)").extract_first()
            date = dateparser.parse(
                element.xpath(self.DATE_XPATH).extract_first(), languages=["pt"]
            ).date()

            yield Gazette(
                date=date,
                file_urls=[url],
                is_extra_edition=False,
                territory_id=self.TERRITORY_ID,
                power="executive",
                scraped_at=datetime.utcnow(),
            )

        current_page = w3lib.url.url_query_parameter(response.url, "pg")

        if (
            not response.css(self.LAST_PAGE_CSS)
            .extract_first()
            .endswith("pg=" + current_page)
        ):
            next_url = w3lib.url.add_or_replace_parameter(
                response.url, "pg", str(int(current_page) + 1)
            )
            yield Request(next_url)
