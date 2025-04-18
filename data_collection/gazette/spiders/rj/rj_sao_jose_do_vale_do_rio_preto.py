from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class RjSaoJoseDoValeDoRioPretoSpider(BaseDospSpider):
    TERRITORY_ID = "3305158"
    name = "rj_sao_jose_do_vale_do_rio_preto"
    start_urls = [
        "https://www.imprensaoficialmunicipal.com.br/sao_jose_do_vale_do_rio_preto"
    ]
    start_date = date(2023, 5, 24)
