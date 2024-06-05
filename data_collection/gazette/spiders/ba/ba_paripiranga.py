from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaParipirangaSpider(SaiGazetteSpider):
    TERRITORY_ID = "2923803"
    name = "ba_paripiranga"
    allowed_domains = ["paripiranga.ba.gov.br"]
    base_url = "https://www.paripiranga.ba.gov.br"
    start_date = date(2008, 1, 22)
