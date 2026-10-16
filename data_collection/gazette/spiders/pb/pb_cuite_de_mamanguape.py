from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class PbCuiteDeMamanguapeSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2505238"
    name = "pb_cuite_de_mamanguape"
    allowed_domains = ["cuitedemamanguape.pb.gov.br"]
    BASE_URL = "https://www.cuitedemamanguape.pb.gov.br"
    start_date = date(2024, 1, 2)
