from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaNiloPecanhaSpider(SaiGazetteSpider):
    TERRITORY_ID = "2922607"
    name = "ba_nilo_pecanha"
    allowed_domains = ["nilopecanha.ba.gov.br"]
    base_url = "https://www.nilopecanha.ba.gov.br"
    start_date = date(2007, 1, 15)
