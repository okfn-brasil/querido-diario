from datetime import date

from gazette.spiders.base.municipioonline import BaseMunicipioOnlineSpider


class SeCampoDoBritoSpider(BaseMunicipioOnlineSpider):
    TERRITORY_ID = "2801009"
    name = "se_campo_do_brito"
    start_date = date(2021, 1, 5)
    url_uf = "se"
    url_city = "campodobrito"
