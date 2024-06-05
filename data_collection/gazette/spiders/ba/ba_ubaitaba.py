from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaUbaitabaSpider(SaiGazetteSpider):
    TERRITORY_ID = "2932200"
    name = "ba_ubaitaba"
    allowed_domains = ["ubaitaba.ba.gov.br"]
    base_url = "https://www.ubaitaba.ba.gov.br"
    start_date = date(2007, 6, 29)
