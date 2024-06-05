from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaIbirapuaSpider(SaiGazetteSpider):
    TERRITORY_ID = "2912806"
    name = "ba_ibirapua"
    allowed_domains = ["ibirapua.ba.gov.br"]
    base_url = "https://www.ibirapua.ba.gov.br"
    start_date = date(2009, 1, 14)
