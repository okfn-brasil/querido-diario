from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaMutuipeSpider(SaiGazetteSpider):
    TERRITORY_ID = "2922409"
    name = "ba_mutuipe"
    allowed_domains = ["mutuipe.ba.gov.br"]
    base_url = "https://www.mutuipe.ba.gov.br"
    start_date = date(2007, 1, 30)
