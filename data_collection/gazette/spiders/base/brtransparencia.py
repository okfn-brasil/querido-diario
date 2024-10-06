import re
from datetime import datetime

from scrapy import Request
from scrapy.selector import Selector

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class BaseBrTransparenciaSpider(BaseGazetteSpider):
    name = ""
    TERRITORY_ID = ""
    allowed_domains = []
    start_urls = [""]
    power = "executive"

    def _extract_entity_code(self, response):
        response_text = response.text
        try:
            intermediate_response_entity = re.search(
                r'var entity="[\d\w\-]+"',
                response_text,
                re.IGNORECASE,
            ).group()
            response_entity = (
                re.search(
                    r'"[\d\w\-]+"',
                    intermediate_response_entity,
                )
                .group()
                .replace('"', "")
            )
        except AttributeError as exc:
            raise AttributeError("Was not possible to extract the entity code") from exc
        try:
            intermediate_response_code = re.search(
                r'var code="[\d\w\-]+"',
                response_text,
                re.IGNORECASE,
            ).group()
            response_code = (
                re.search(r'"[\d\w\-]+"', intermediate_response_code)
                .group()
                .replace('"', "")
            )
        except AttributeError as exc:
            raise AttributeError("Was not possible to extract the code") from exc

        api_url = f"https://api.brtransparencia.com.br/api/diariooficial/filtro/{response_entity}/{response_code}/{self.start_date}/{self.end_date}/-1/-1"
        yield Request(api_url)

    def start_requests(self):
        # getting the entity and code from inner JS Content file
        url = self.start_urls[0].replace("/diario.html", "/js/content.js")

        yield Request(url, callback=self._extract_entity_code)

    def parse(self, response):
        for entry in response.json():
            edition_date = datetime.strptime(
                entry["dat_publicacao_dio"], "%Y-%m-%dT%H:%M:%S"
            ).date()
            extra_edition = True if entry["des_extra_dio"] is not None else False
            edition_number = int(entry["num_diario_oficial_dio"])
            gezzetes = Selector(text=entry["des_resumo_dio"]).css("a")
            urls = []
            for item in gezzetes:
                link = item.css("a::attr(href)").get()
                urls.append(link)

            yield Gazette(
                edition_number=edition_number,
                date=edition_date,
                file_urls=urls,
                is_extra_edition=extra_edition,
                power=self.power,
            )
