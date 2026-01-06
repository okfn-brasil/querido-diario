from datetime import date

from gazette.spiders.base.municipioonline import BaseMunicipioOnlineSpider


class SeSiririSpider(BaseMunicipioOnlineSpider):
    TERRITORY_ID = "2807204"
    name = "se_siriri"
    url_uf = "se"
    url_city = "siriri"
    start_date = date(2017, 1, 3)
