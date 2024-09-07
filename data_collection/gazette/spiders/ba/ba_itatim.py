import datetime as dt

from gazette.spiders.base.sai import SaiGazetteSpider


class BaMaragogipeSpider(SaiGazetteSpider):
    TERRITORY_ID = "2916856"
    name = "ba_itatim"
    start_date = dt.date(2009, 1, 1)
    allowed_domains = ["sai.io.org.br", "www.itatim.ba.gov.br"]
    base_url = "https://www.itatim.ba.gov.br"
