from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaItuberaSpider(SaiGazetteSpider):
    TERRITORY_ID = "2917300"
    name = "ba_itubera"
    allowed_domains = ["itubera.ba.gov.br"]
    base_url = "https://www.itubera.ba.gov.br"
    start_date = date(2003, 9, 30)
