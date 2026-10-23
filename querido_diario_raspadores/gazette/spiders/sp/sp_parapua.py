from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpParapuaSpider(BaseDospSpider):
    TERRITORY_ID = "3536000"
    name = "sp_parapua"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/parapua"]
    start_date = date(2021, 12, 23)
