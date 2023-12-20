from datetime import date

from gazette.spiders.base.municipioonline import BaseMunicipioOnlineSpider


class SePocoVerdeSpider(BaseMunicipioOnlineSpider):
    TERRITORY_ID = "2805505"
    name = "se_poco_verde"
    start_date = date(2023, 1, 2)
    url_uf = "se"
    url_city = "pocoverde"
