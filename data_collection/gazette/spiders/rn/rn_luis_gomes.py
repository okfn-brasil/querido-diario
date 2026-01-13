from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class RnLuisGomesSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2407005"
    name = "rn_luis_gomes"
    allowed_domains = ["luisgomes.rn.gov.br"]
    BASE_URL = "https://www.luisgomes.rn.gov.br"
    start_date = date(2018, 4, 3)
