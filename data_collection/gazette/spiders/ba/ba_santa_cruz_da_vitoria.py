from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaSantaCruzDaVitoriaSpider(SaiGazetteSpider):
    TERRITORY_ID = "2927804"
    name = "ba_santa_cruz_da_vitoria"
    allowed_domains = ["santacruzdavitoria.ba.gov.br"]
    base_url = "https://www.santacruzdavitoria.ba.gov.br"
    start_date = date(2006, 1, 27)
