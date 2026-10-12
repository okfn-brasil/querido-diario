from datetime import date

from gazette.spiders.base.municipioonline import BaseMunicipioOnlineSpider


class SePacatubaSpider(BaseMunicipioOnlineSpider):
    TERRITORY_ID = "2804904"
    name = "se_pacatuba"
    url_uf = "se"
    url_city = "pacatuba"
    start_date = date(2026, 1, 8)
