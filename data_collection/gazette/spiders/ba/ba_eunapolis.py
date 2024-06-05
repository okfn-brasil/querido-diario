from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaEunapolisSpider(SaiGazetteSpider):
    TERRITORY_ID = "2910727"
    name = "ba_eunapolis"
    allowed_domains = ["eunapolis.ba.gov.br"]
    base_url = "https://www.eunapolis.ba.gov.br"
    start_date = date(2010, 1, 15)
