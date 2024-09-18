from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaGongogi(SaiGazetteSpider):
    name = "ba_gongogi"
    allowed_domains = ["gongogi.ba.gov.br"]
    start_date = date(2005, 8, 15)
    base_url = "https://www.gongogi.ba.gov.br"
    TERRITORY_ID = "2911501"
