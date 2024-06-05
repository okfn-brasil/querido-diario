from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaSeabraSpider(SaiGazetteSpider):
    TERRITORY_ID = "2929909"
    name = "ba_seabra"
    allowed_domains = ["sai.io.org.br"]
    base_url = "https://sai.io.org.br/ba/seabra"
    start_date = date(2009, 2, 11)
