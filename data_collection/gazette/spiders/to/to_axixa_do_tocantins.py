from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class ToAxixaDoTocantinsSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "1702901"
    name = "to_axixa_do_tocantins"
    allowed_domains = ["www.axixa.to.gov.br"]
    BASE_URL = "https://www.axixa.to.gov.br"
    start_date = date(2021, 8, 16)
