from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class PrAntonioOlintoSpider(BaseInstarSpider):
    TERRITORY_ID = "4101309"
    name = "pr_antonio_olinto"
    base_url = "https://antonioolinto.pr.gov.br/portal/diario-oficial"
    start_date = date(2016, 6, 14)
