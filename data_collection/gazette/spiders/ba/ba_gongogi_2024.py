from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaGongogiSaiGazetteSpider(SaiGazetteSpider):
    name = "ba_gongogi_2024"
    allowed_domains = ["gongogi.ba.gov.br"]
    start_date = date(2024, 1, 1)
    base_url = "https://www.gongogi.ba.gov.br"
    TERRITORY_ID = "2911501"
