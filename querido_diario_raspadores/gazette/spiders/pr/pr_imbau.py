from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class PrImbauSpider(BaseInstarSpider):
    TERRITORY_ID = "4110078"
    name = "pr_imbau"
    base_url = "https://www.imbau.pr.gov.br/portal/diario-oficial"
    start_date = date(2015, 5, 29)
