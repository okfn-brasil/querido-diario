from datetime import date

from gazette.spiders.base.municipioonline import BaseMunicipioOnlineSpider


class SePedrinhasSpider(BaseMunicipioOnlineSpider):
    TERRITORY_ID = "2805109"
    name = "se_pedrinhas"
    url_uf = "se"
    url_city = "pedrinhas"
    start_date = date(2018, 2, 7)
