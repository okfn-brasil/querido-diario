from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaMansidaoSpider(SaiGazetteSpider):
    TERRITORY_ID = "2920452"
    name = "ba_mansidao"
    allowed_domains = ["mansidao.ba.gov.br"]
    base_url = "https://www.mansidao.ba.gov.br"
    start_date = date(2021, 2, 24)
