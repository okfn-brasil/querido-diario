from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpIpuaSpider(BaseDospSpider):
    TERRITORY_ID = "3521309"
    name = "sp_ipua"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/ipua"]
    start_date = date(2019, 12, 12)
