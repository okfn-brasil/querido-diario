from datetime import date

from gazette.spiders.base.municipioonline import BaseMunicipioOnlineSpider


class SeFreiPauloSpider(BaseMunicipioOnlineSpider):
    TERRITORY_ID = "2802304"
    name = "se_frei_paulo"
    url_uf = "se"
    url_city = "freipaulo"
    start_date = date(2022, 1, 14)
