from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaPiripaSpider(SaiGazetteSpider):
    TERRITORY_ID = "2924702"
    name = "ba_piripa"
    allowed_domains = ["piripa.ba.gov.br"]
    base_url = "https://www.piripa.ba.gov.br"
    start_date = date(2007, 3, 13)
