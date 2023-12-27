import datetime

from gazette.spiders.base.diariooficialbr import BaseDiarioOficinalBRSpider


class ToAguiarnopolisSpider(BaseDiarioOficinalBRSpider):
    TERRITORY_ID = "1700301"
    name = "to_aguiarnopolis"
    allowed_domains = ["diariooficial.aguiarnopolis.to.gov.br"]
    start_date = datetime.date(2020, 1, 23)
    city_domain = "diariooficial.aguiarnopolis.to.gov.br"
    url_base = "https://diariooficial.aguiarnopolis.to.gov.br"
