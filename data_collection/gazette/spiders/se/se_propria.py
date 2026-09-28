from datetime import date

from gazette.spiders.base.municipioonline import BaseMunicipioOnlineSpider


class SePropriaSpider(BaseMunicipioOnlineSpider):
    TERRITORY_ID = "2805703"
    name = "se_propria"
    url_uf = "se"
    url_city = "propria"
    start_date = date(2021, 2, 23)
