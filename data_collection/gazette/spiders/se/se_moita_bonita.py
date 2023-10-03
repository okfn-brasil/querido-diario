from datetime import date

from gazette.spiders.base.municipioonline import BaseMunicipioOnlineSpider


class SeMoitaBonitaSpider(BaseMunicipioOnlineSpider):
    TERRITORY_ID = "2804102"
    name = "se_moita_bonita"
    start_date = date(2022, 2, 17)
    url_uf = "se"
    url_city = "moitabonita"
