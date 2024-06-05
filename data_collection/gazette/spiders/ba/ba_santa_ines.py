from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaSantaInesSpider(SaiGazetteSpider):
    TERRITORY_ID = "2927903"
    name = "ba_santa_ines"
    allowed_domains = ["santaines.ba.gov.br"]
    base_url = "https://www.santaines.ba.gov.br"
    start_date = date(2007, 6, 5)
