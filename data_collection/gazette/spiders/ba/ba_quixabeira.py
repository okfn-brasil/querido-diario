from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaQuixabeiraSpider(SaiGazetteSpider):
    TERRITORY_ID = "2925931"
    name = "ba_quixabeira"
    allowed_domains = ["quixabeira.ba.gov.br"]
    base_url = "https://www.quixabeira.ba.gov.br"
    start_date = date(2007, 10, 23)
