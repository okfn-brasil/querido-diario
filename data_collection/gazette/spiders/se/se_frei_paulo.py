from datetime import date

from gazette.spiders.base.municipioonline import BaseMunicipioOnlineSpider


class SeFreiPaulo(BaseMunicipioOnlineSpider):
    TERRITORY_ID = "2802304"
    name = "se_frei_paulo"
    start_date = date(2022, 1, 14)
    url_uf = "se"
    url_city = "freipaulo"
