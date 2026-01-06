from datetime import date

from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider
from gazette.utils.extraction import get_date_from_text


class RrBoaVistaSpider(BaseGazetteSpider):
    TERRITORY_ID = "1400100"
    name = "rr_boa_vista"
    allowed_domains = ["boavista.rr.gov.br"]
    start_urls = ["https://publicacoes.boavista.rr.gov.br/api/v1/diarios"]
    start_date = date(2010, 6, 14)
    custom_settings = {"DOWNLOAD_DELAY": 2.0}  # prevent 429 (too many requests)

    def parse(self, response, page=1):
        for entry in response.json()["data"]:
            raw_date = entry["data"].split(", ")[-1]
            date = get_date_from_text(raw_date)

            if date < self.start_date:
                return

            edition_number = entry["edicao"]
            url = response.urljoin(entry["media"]["url"])
            yield Gazette(
                file_urls=[url],
                date=date,
                edition_number=edition_number,
                power="executive",
            )

        next_page = page + 1
        yield Request(
            f"https://publicacoes.boavista.rr.gov.br/api/v1/diarios?page={next_page}",
            cb_kwargs={"page": next_page},
        )
