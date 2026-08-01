from datetime import date

from gazette.spiders.base.municipioonline import BaseMunicipioOnlineSpider


class SeTelhaSpider(BaseMunicipioOnlineSpider):
    TERRITORY_ID = "2807303"
    name = "se_telha"
    url_uf = "se"
    url_city = "telha"
    start_date = date(2017, 1, 20)
