from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class MsGloriaDeDouradosSpider(BaseDospSpider):
    TERRITORY_ID = "5004007"
    name = "ms_gloria_de_dourados"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/gloria_de_dourados"]
    start_date = date(2023, 11, 7)
