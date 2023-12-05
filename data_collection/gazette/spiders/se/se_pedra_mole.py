from datetime import date

from gazette.spiders.base.municipioonline import BaseMunicipioOnlineSpider


class SePedraMole(BaseMunicipioOnlineSpider):
    TERRITORY_ID = "2805000"
    name = "se_pedra_mole"
    start_date = date(2017, 1, 26)
    url_uf = "se"
    url_city = "pedramole"
