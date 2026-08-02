from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class CeGeneralSampaioSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2304608"
    name = "ce_general_sampaio"
    allowed_domains = ["generalsampaio.ce.gov.br"]
    BASE_URL = "https://www.generalsampaio.ce.gov.br"
    start_date = date(2016, 9, 15)
