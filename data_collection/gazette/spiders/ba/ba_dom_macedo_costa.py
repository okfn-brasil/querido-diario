from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaDomMacedoCostaSpider(SaiGazetteSpider):
    TERRITORY_ID = "2910206"
    name = "ba_dom_macedo_costa"
    allowed_domains = ["dommacedocosta.ba.gov.br"]
    base_url = "https://www.dommacedocosta.ba.gov.br"
    start_date = date(2010, 1, 6)
