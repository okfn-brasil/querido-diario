from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpMonteAltoSpider(BaseInstarSpider):
    TERRITORY_ID = "3531308"
    name = "sp_monte_alto_2017"
    allowed_domains = ["montealto.instaridc.com.br"]
    base_url = "https://www.montealto.instaridc.com.br/portal/diario-oficial"
    start_date = date(2017, 9, 11)
