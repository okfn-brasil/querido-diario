from datetime import date

from gazette.spiders.base.municipioonline import BaseMunicipioOnlineSpider


class SeMuribecaSpider(BaseMunicipioOnlineSpider):
    TERRITORY_ID = "2804300"
    name = "se_muribeca"
    url_uf = "se"
    url_city = "muribeca"
    start_date = date(2019, 5, 20)
