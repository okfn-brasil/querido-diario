from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpSaoJoaquimDaBarraSpider(BaseDospSpider):
    TERRITORY_ID = "3549409"
    name = "sp_sao_joaquim_da_barra"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/sao_joaquim_da_barra"]
    start_date = date(2017, 5, 26)
