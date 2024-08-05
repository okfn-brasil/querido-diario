from datetime import date

from gazette.spiders.base.brtransparencia import BaseBrTransparenciaSpider


class BaPortoSeguroSpider(BaseBrTransparenciaSpider):
    name = "ba_porto_seguro"
    TERRITORY_ID = "2925303"
    allowed_domains = ["cmportoseguroba.brtransparencia.com.br"]
    start_urls = ["https://cmportoseguroba.brtransparencia.com.br/diario.html"]
    start_date = date(2022, 12, 19)
    br_tranparencia_entity = "4557886f-5713-4999-b2c5-c54d9ee11b44"
    br_tranparencia_code = "COD_ENT_CM210"
    power = "legislative"
