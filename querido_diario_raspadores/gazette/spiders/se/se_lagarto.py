from datetime import date

from gazette.spiders.base.municipioonline import BaseMunicipioOnlineSpider


class SeLagartoSpider(BaseMunicipioOnlineSpider):
    TERRITORY_ID = "2803500"
    name = "se_lagarto"
    url_uf = "se"
    url_city = "lagarto"
    start_date = date(2025, 6, 27)
