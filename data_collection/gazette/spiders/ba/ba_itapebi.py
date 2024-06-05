from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaItapebiSpider(SaiGazetteSpider):
    TERRITORY_ID = "2916302"
    name = "ba_itapebi"
    allowed_domains = ["itapebi.ba.gov.br"]
    base_url = "https://www.itapebi.ba.gov.br"
    start_date = date(2005, 5, 8)
