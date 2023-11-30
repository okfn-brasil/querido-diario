from datetime import date

from gazette.spiders.base.municipioonline import BaseMunicipioOnlineSpider


class SeSaoDomingosSpider(BaseMunicipioOnlineSpider):
    TERRITORY_ID = "2806800"
    name = "se_sao_domingos"
    start_date = date(2021, 1, 12)
    url_uf = "se"
    url_city = "saodomingos"
