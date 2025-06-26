from datetime import date

from gazette.spiders.base.brtransparencia import BaseBrTransparenciaSpider


class BaPortoSeguroSpider(BaseBrTransparenciaSpider):
    name = "ba_porto_seguro"
    TERRITORY_ID = "2925303"
    allowed_domains = [
        "cmportoseguroba.brtransparencia.com.br",
        "api.brtransparencia.com.br",
    ]
    start_urls = ["https://cmportoseguroba.brtransparencia.com.br/diario.html"]
    start_date = date(2022, 12, 19)
    power = "legislative"
