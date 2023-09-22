import datetime

from gazette.spiders.base.adiarios import AdiariosGazetteSpider


class MaBuriticupu(AdiariosGazetteSpider):
    name = "ma_buriticupu"
    allowed_domains = ["buriticupu.ma.gov.br"]
    start_date = datetime.date(2018, 5, 7)

    TERRITORY_ID = "2102325"
    BASE_URL = "http://www.buriticupu.ma.gov.br"
