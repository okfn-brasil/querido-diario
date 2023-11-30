from datetime import date

from gazette.spiders.base.municipioonline import BaseMunicipioOnlineSpider


class SeSimaoDiasSpider(BaseMunicipioOnlineSpider):
    TERRITORY_ID = "2807105"
    name = "se_simao_dias"
    start_date = date(2021, 1, 4)
    url_uf = "se"
    url_city = "simaodias"
