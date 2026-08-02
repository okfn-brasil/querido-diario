from datetime import date

from gazette.spiders.base.municipioonline import BaseMunicipioOnlineSpider


class SePedraMoleSpider(BaseMunicipioOnlineSpider):
    TERRITORY_ID = "2805000"
    name = "se_pedra_mole"
    url_uf = "se"
    url_city = "pedramole"
    start_date = date(2017, 1, 26)
