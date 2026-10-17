from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpAltinopolisSpider(BaseDospSpider):
    TERRITORY_ID = "3501004"
    name = "sp_altinopolis"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/altinopolis"]
    start_date = date(2017, 9, 4)
