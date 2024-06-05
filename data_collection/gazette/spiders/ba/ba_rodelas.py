from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaRodelasSpider(SaiGazetteSpider):
    TERRITORY_ID = "2927101"
    name = "ba_rodelas"
    allowed_domains = ["rodelas.ba.gov.br"]
    base_url = "https://www.rodelas.ba.gov.br"
    start_date = date(2018, 8, 24)
