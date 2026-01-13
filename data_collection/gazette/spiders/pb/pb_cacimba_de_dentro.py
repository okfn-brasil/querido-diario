from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class PbCacimbaDeDentroSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2503506"
    name = "pb_cacimba_de_dentro"
    allowed_domains = ["cacimbadedentro.pb.gov.br"]
    BASE_URL = "https://www.cacimbadedentro.pb.gov.br"
    start_date = date(2024, 2, 5)
