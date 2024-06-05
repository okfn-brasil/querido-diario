from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaJaguaripeSpider(SaiGazetteSpider):
    TERRITORY_ID = "2917805"
    name = "ba_jaguaripe"
    allowed_domains = ["jaguaripe.ba.gov.br"]
    base_url = "https://www.jaguaripe.ba.gov.br"
    start_date = date(2008, 12, 30)
