from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaCamamuSpider(SaiGazetteSpider):
    TERRITORY_ID = "2905800"
    name = "ba_camamu"
    allowed_domains = ["camamu.ba.gov.br"]
    base_url = "https://www.camamu.ba.gov.br"
    start_date = date(2009, 1, 2)
