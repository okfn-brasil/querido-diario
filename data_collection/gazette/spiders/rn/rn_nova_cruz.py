from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class RnNovaCruzSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2408300"
    name = "rn_nova_cruz"
    allowed_domains = ["novacruz.rn.gov.br"]
    BASE_URL = "https://www.novacruz.rn.gov.br"
    start_date = date(2013, 4, 1)
