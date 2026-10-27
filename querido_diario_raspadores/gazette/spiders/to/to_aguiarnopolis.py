import datetime

from gazette.spiders.base.govweb import BaseGovWebSpider


class ToAguiarnopolisSpider(BaseGovWebSpider):
    TERRITORY_ID = "1700301"
    name = "to_aguiarnopolis"
    start_date = datetime.date(2020, 1, 23)
    base_url = "https://www.aguiarnopolis.to.gov.br"
