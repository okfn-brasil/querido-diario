from datetime import date

from gazette.spiders.base.sai import BaseSaiSpider


class BaAratacaSpider(BaseSaiSpider):
    TERRITORY_ID = "2902609"
    name = "ba_baixa_grande"
    allowed_domains = ["baixagrande.ba.gov.br"]
    base_url = "https://www.baixagrande.ba.gov.br"
    start_date = date(2010, 1, 15)
