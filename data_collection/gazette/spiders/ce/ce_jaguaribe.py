from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class CeJaguaribeSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2306900"
    name = "ce_jaguaribe"
    allowed_domains = ["jaguaribe.ce.gov.br"]
    BASE_URL = "https://www.jaguaribe.ce.gov.br"
    start_date = date(2006, 6, 23)
