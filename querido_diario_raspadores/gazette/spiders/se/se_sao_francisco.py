from datetime import date

from gazette.spiders.base.municipioonline import BaseMunicipioOnlineSpider


class SeSaoFranciscoSpider(BaseMunicipioOnlineSpider):
    TERRITORY_ID = "2806909"
    name = "se_sao_francisco"
    url_uf = "se"
    url_city = "saofrancisco"
    start_date = date(2025, 1, 2)
