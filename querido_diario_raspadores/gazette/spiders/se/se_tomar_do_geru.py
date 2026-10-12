from datetime import date

from gazette.spiders.base.municipioonline import BaseMunicipioOnlineSpider


class SeTomarDoGeruSpider(BaseMunicipioOnlineSpider):
    TERRITORY_ID = "2807501"
    name = "se_tomar_do_geru"
    url_uf = "se"
    url_city = "tomardogeru"
    start_date = date(2025, 1, 2)
