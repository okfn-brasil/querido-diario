from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaNovaFatimaSpider(SaiGazetteSpider):
    TERRITORY_ID = "2922730"
    name = "ba_nova_fatima"
    allowed_domains = ["fatima.ba.gov.br"]
    base_url = "https://www.fatima.ba.gov.br"
    start_date = date(2007, 7, 11)
