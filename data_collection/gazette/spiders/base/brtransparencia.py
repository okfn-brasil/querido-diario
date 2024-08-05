from datetime import datetime

from scrapy import Request
from scrapy.selector import Selector

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class BaseBrTransparenciaSpider(BaseGazetteSpider):
    name = ""
    TERRITORY_ID = ""
    allowed_domains = [""]
    start_urls = [""]
    br_tranparencia_entity = ""
    br_tranparencia_code = ""
    power = "executive"

    def start_requests(self):
        api_url = f"https://api.brtransparencia.com.br/api/diariooficial/filtro/{self.br_tranparencia_entity}/{self.br_tranparencia_code}/{self.start_date}/{self.end_date}/-1/-1"

        yield Request(api_url)

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
