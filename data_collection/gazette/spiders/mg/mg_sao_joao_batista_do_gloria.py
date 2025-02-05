from datetime import date

from gazette.spiders.base.rgsites import BaseRgSites


class MgSaoJoaoBatistaDoGloriaSpider(BaseRgSites):
    name = "mg_sao_joao_batista_do_gloria"
    TERRITORY_ID = "3162203"
    allowed_domains = ["www.gloria.mg.gov.br"]
    BASE_URL = "https://www.gloria.mg.gov.br/diario-oficial"
    start_date = date(2019, 1, 3)
