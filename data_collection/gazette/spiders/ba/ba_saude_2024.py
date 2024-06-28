from datetime import date

from gazette.spiders.base.brtransparencia import BaseBrTransparenciaSpider


class BaSaudeSpider(BaseBrTransparenciaSpider):
    name = "ba_saude_2024"
    TERRITORY_ID = "2929800"
    allowed_domains = ["pmsaudeba.brtransparencia.com.br"]
    start_urls = ["https://pmsaudeba.brtransparencia.com.br/diario.html"]
    start_date = date(2024, 1, 31)
    br_tranparencia_entity = "46366dbc-7780-433d-a689-f287561a8a7a"
    br_tranparencia_code = "COD_ENT_PM005"
    power = "executive"
