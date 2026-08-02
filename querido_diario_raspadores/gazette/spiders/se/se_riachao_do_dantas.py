from datetime import date

from gazette.spiders.base.municipioonline import BaseMunicipioOnlineSpider


class SeRiachaoDoDantasSiririSpider(BaseMunicipioOnlineSpider):
    TERRITORY_ID = "2805802"
    name = "se_riachao_do_dantas"
    start_date = date(2018, 11, 14)
    url_uf = "se"
    url_city = "riachaododantas"
