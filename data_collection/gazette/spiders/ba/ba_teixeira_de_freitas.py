from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaTeixeiraDeFreitasSpider(SaiGazetteSpider):
    TERRITORY_ID = "2931350"
    name = "ba_teixeira_de_freitas"
    allowed_domains = ["sai.io.org.br"]
    base_url = "https://sai.io.org.br/ba/teixeiradefreitas"
    start_date = date(2007, 9, 11)
