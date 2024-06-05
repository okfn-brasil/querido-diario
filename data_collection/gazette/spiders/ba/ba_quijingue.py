from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaQuijingueSpider(SaiGazetteSpider):
    TERRITORY_ID = "2925907"
    name = "ba_quijingue"
    allowed_domains = ["quijingue.ba.gov.br"]
    base_url = "https://www.quijingue.ba.gov.br"
    start_date = date(2007, 8, 15)
