from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class PrJabotiSpider(BaseInstarSpider):
    TERRITORY_ID = "4111704"
    name = "pr_jaboti"
    allowed_domains = ["jaboti.pr.gov.br"]
    base_url = "https://www.jaboti.pr.gov.br/portal/diario-oficial"
    start_date = date(2018, 1, 3)
