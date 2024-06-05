from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaFlorestaAzulSpider(SaiGazetteSpider):
    TERRITORY_ID = "2911006"
    name = "ba_floresta_azul"
    allowed_domains = ["florestaazul.ba.gov.br"]
    base_url = "https://www.florestaazul.ba.gov.br"
    start_date = date(2007, 5, 30)
