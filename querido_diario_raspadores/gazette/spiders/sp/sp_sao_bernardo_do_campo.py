from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpSaoBernardoDoCampoSpider(BaseDospSpider):
    TERRITORY_ID = "3548708"
    name = "sp_sao_bernardo_do_campo"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/sao_bernardo_do_campo"]
    start_date = date(2017, 5, 12)
