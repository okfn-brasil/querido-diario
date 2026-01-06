from datetime import date

from gazette.spiders.base.municipioonline import BaseMunicipioOnlineSpider


class SeCanindeDeSaoFranciscoSpider(BaseMunicipioOnlineSpider):
    TERRITORY_ID = "2801207"
    name = "se_caninde_de_sao_francisco"
    url_uf = "se"
    url_city = "canindedesaofrancisco"
    start_date = date(2017, 1, 2)
