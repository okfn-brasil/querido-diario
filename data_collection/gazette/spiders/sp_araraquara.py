import datetime
from urllib.parse import urlencode

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class SpAraraquaraSpider(BaseGazetteSpider):
    TERRITORY_ID = "3503208"
    name = "sp_araraquara"
    allowed_domains = ["diariooficialcmararaquara.sp.gov.br"]
    start_date = datetime.date(2021, 3, 4)  # First gazette available
    end_date = datetime.datetime.today()
    start_urls = ["https://www.diariooficialcmararaquara.sp.gov.br/diario/busca?"]

    base_url = "https://www.diariooficialcmararaquara.sp.gov.br"

    def parse(self, response):

        initial = self.start_date.strftime("%d/%m/%Y")
        end = self.end_date.strftime("%d/%m/%Y")

        params = {
            "data": initial,
            "dataFinal": end,
            "descricao": "",
            "subcategoria": "",
        }
        url_params = urlencode(params)
        response.follow(f"{self.start_urls}{url_params}", self.parse_gazette)

    def parse_gazette(self, response):

        gazettes = response.css(".event-card.animated.flipInX")

        for gazette in gazettes:
            card = gazette.css(".event-card")

            edition_number = card.css("event-data h4 ::text").re_first(r"[0-9]+")
            date = card.re_first(r"[0-9]+/[0-9]+/[0-9]+")
            url = card.css(".row ::attr(href)").get()
            url = base_url + url
            if card.css(".event-edicao p ::text").get() == "Edição Única":
                extra_edition = False
            else:
                extra_edition = True

            yield Gazette(
                date=date,
                file_urls=[url],
                is_extra_edition=extra_edition,
                power="executive",
                edition_number=edition_number,
            )
