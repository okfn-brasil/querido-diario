from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class MgCarmoDaCachoeiraSpider(BaseInstarSpider):
    TERRITORY_ID = "3113909"
    name = "mg_carmo_da_cachoeira"
    allowed_domains = ["carmodacachoeira.mg.gov.br"]
    base_url = "https://www.carmodacachoeira.mg.gov.br/portal/diario-oficial"
    start_date = date(2018, 1, 3)
