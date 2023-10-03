from datetime import date

from gazette.spiders.base.municipioonline import BaseMunicipioOnlineSpider


class SeMacambiraSpider(BaseMunicipioOnlineSpider):
    TERRITORY_ID = "2803708"
    name = "se_macambira"
    start_date = date(2019, 1, 22)
    url_uf = "se"
    url_city = "macambira"
