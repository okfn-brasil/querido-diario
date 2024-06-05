from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaItirucuSpider(SaiGazetteSpider):
    TERRITORY_ID = "2916906"
    name = "ba_itirucu"
    allowed_domains = ["itirucu.ba.gov.br"]
    base_url = "https://www.itirucu.ba.gov.br"
    start_date = date(2006, 9, 13)
