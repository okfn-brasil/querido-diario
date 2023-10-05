from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpMonteAltoSpider(BaseInstarSpider):
    TERRITORY_ID = "3531308"
    name = "sp_monte_alto_2017"
    allowed_domains = ["montealto.instaridc.com.br"]
    start_date = date(2017, 9, 11)
    base_url = "http://montealto.instaridc.com.br/portal/diario-oficial"
