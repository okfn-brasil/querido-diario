from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpMairinqueSpider(BaseInstarSpider):
    TERRITORY_ID = "3528403"
    name = "sp_mairinque"
    base_url = "https://www.mairinque.sp.gov.br/portal/diario-oficial"
    start_date = date(2024, 1, 19)
