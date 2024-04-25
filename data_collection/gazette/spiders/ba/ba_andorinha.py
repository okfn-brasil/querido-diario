import datetime as dt

from gazette.spiders.base.sai import SaiGazetteSpider


class BaAndorinhaSpider(SaiGazetteSpider):
    TERRITORY_ID = "2901353"
    name = "ba_andorinha"
    start_date = dt.date(2013, 1, 2)
    allowed_domains = ["adorinha.ba.gov.br"]
    base_url = "https://www.andorinha.ba.gov.br/site/diariooficial"
