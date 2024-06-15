from datetime import date

from gazette.spiders.base.municipioonline import BaseMunicipioOnlineSpider


class SeAquidabaSpider(BaseMunicipioOnlineSpider):
    TERRITORY_ID = "2800209"
    name = "se_aquidaba"
    url_uf = "se"
    url_city = "aquidaba"
    start_date = date(2017, 2, 16)
