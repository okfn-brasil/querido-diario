from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaNovaSoureSpider(SaiGazetteSpider):
    TERRITORY_ID = "2922904"
    name = "ba_nova_soure"
    allowed_domains = ["novasoure.ba.gov.br"]
    base_url = "https://www.novasoure.ba.gov.br"
    start_date = date(2008, 10, 7)
