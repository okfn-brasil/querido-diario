from datetime import date

from gazette.spiders.base.dionet import BaseDionetSpider


class EsEstadoSpider(BaseDionetSpider):
    TERRITORY_ID = "3299999"
    name = "es_estado"
    start_date = date(2003, 3, 17)

    BASE_URL = "https://ioes.dio.es.gov.br"

    custom_settings = {"DOWNLOAD_DELAY": 0.5, "RANDOMIZE_DOWNLOAD_DELAY": True}

    def parse(self, response, gazette_date):
        for gazette in super().parse(response, gazette_date):
            # Editions up to February 2014 are listed with `numero = 0`
            if not gazette["edition_number"]:
                del gazette["edition_number"]

            yield gazette
