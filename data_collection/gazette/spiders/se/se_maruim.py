from datetime import date

from gazette.spiders.base.municipioonline import BaseMunicipioOnlineSpider


class SeMaruimSpider(BaseMunicipioOnlineSpider):
    TERRITORY_ID = "2804003"
    name = "se_maruim"
    url_uf = "se"
    url_city = "maruim"
    start_date = date(2023, 1, 2)
