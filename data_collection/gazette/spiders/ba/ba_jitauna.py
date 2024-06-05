from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaJitaunaSpider(SaiGazetteSpider):
    TERRITORY_ID = "2918308"
    name = "ba_jitauna"
    allowed_domains = ["jitauna.ba.gov.br"]
    base_url = "https://www.jitauna.ba.gov.br"
    start_date = date(2005, 6, 9)
