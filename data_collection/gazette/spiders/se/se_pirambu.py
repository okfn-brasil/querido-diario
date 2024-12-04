from datetime import date

from gazette.spiders.base.municipioonline import BaseMunicipioOnlineSpider


class SePirambuSpider(BaseMunicipioOnlineSpider):
    TERRITORY_ID = "2805307"
    name = "se_pirambu"
    url_uf = "se"
    url_city = "pirambu"
    start_date = date(2017, 3, 9)
