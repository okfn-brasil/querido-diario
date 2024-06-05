from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaIbicoaraSpider(SaiGazetteSpider):
    TERRITORY_ID = "2912202"
    name = "ba_ibicoara"
    allowed_domains = ["ibicoara.ba.gov.br"]
    base_url = "https://www.ibicoara.ba.gov.br"
    start_date = date(2013, 1, 2)
