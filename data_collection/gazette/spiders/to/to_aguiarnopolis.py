import datetime

from gazette.spiders.base.diariooficialbr import BaseDiarioOficialBRSpider


class ToAguiarnopolisSpider(BaseDiarioOficialBRSpider):
    TERRITORY_ID = "1700301"
    name = "to_aguiarnopolis"
    allowed_domains = ["diariooficial.aguiarnopolis.to.gov.br"]
    start_date = datetime.date(2020, 1, 23)
    BASE_URL = "https://diariooficial.aguiarnopolis.to.gov.br"
