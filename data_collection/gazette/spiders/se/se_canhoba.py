from datetime import date

from gazette.spiders.base.municipioonline import BaseMunicipioOnlineSpider


class SeCanhobaSpider(BaseMunicipioOnlineSpider):
    TERRITORY_ID = "2801108"
    name = "se_canhoba"
    url_uf = "se"
    url_city = "canhoba"
    start_date = date(2020, 1, 16)
