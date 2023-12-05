from datetime import date

from gazette.spiders.base.municipioonline import BaseMunicipioOnlineSpider


class SeCapelaSpider(BaseMunicipioOnlineSpider):
    TERRITORY_ID = "2801306"
    name = "se_capela"
    start_date = date(2021, 2, 4)
    url_uf = "se"
    url_city = "capela"
