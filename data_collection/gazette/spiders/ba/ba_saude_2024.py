from datetime import date

from gazette.spiders.base.brtransparencia import BaseBrTransparenciaSpider


class BaSaudeSpider(BaseBrTransparenciaSpider):
    name = "ba_saude_2024"
    TERRITORY_ID = "2929800"
    allowed_domains = ["pmsaudeba.brtransparencia.com.br", "api.brtransparencia.com.br"]
    start_urls = ["https://pmsaudeba.brtransparencia.com.br/diario.html"]
    start_date = date(2024, 1, 31)
    power = "executive"
