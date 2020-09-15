from gazette.spiders.instar_base import BaseInstarSpider


class SpMonteAltoSpider(BaseInstarSpider):
    TERRITORY_ID = "3531308"
    name = "sp_monte_alto"
    allowed_domains = ["montealto.instaridc.com.br"]
    start_urls = ["http://montealto.instaridc.com.br/portal/diario-oficial"]
