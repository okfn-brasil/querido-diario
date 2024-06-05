from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaElisioMedradoSpider(SaiGazetteSpider):
    TERRITORY_ID = "2910305"
    name = "ba_elisio_medrado"
    allowed_domains = ["elisiomedrado.ba.gov.br"]
    base_url = "https://www.elisiomedrado.ba.gov.br"
    start_date = date(2009, 2, 27)
