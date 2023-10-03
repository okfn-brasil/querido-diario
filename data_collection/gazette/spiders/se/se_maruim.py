from datetime import date

from gazette.spiders.base.municipioonline import BaseMunicipioOnlineSpider


class SeMaruimSpider(BaseMunicipioOnlineSpider):
    TERRITORY_ID = "2804003"
    name = "se_maruim"
    start_date = date(2022, 3, 4)
    url_uf = "se"
    url_city = "maruim"
