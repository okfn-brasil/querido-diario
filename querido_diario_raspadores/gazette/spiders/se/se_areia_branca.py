from datetime import date

from gazette.spiders.base.municipioonline import BaseMunicipioOnlineSpider


class SeAreiaBrancaSpider(BaseMunicipioOnlineSpider):
    TERRITORY_ID = "2800506"
    name = "se_areia_branca"
    url_uf = "se"
    url_city = "areiabranca"
    start_date = date(2017, 1, 2)
