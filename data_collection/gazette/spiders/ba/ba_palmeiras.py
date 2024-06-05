from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaPalmeirasSpider(SaiGazetteSpider):
    TERRITORY_ID = "2923506"
    name = "ba_palmeiras"
    allowed_domains = ["palmeiras.ba.gov.br"]
    base_url = "https://www.palmeiras.ba.gov.br"
    start_date = date(2006, 4, 24)
