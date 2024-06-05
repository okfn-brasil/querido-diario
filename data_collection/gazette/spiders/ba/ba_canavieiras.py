from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaCanavieirasSpider(SaiGazetteSpider):
    TERRITORY_ID = "2906303"
    name = "ba_canavieiras"
    allowed_domains = ["canavieiras.ba.gov.br"]
    base_url = "https://www.canavieiras.ba.gov.br"
    start_date = date(2006, 3, 20)
