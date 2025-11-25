from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class RsQuatroIrmaosSpider(BaseDospSpider):
    TERRITORY_ID = "4315313"
    name = "rs_quatro_irmaos"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/quatro_irmaos"]
    start_date = date(2024, 5, 14)
