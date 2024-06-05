from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaPedraoSpider(SaiGazetteSpider):
    TERRITORY_ID = "2924108"
    name = "ba_pedrao"
    allowed_domains = ["pedrao.ba.gov.br"]
    base_url = "https://www.pedrao.ba.gov.br"
    start_date = date(2013, 2, 25)
