from datetime import date

from gazette.spiders.base.municipioonline import BaseMunicipioOnlineSpider


class SeBarraDosCoqueirosSpider(BaseMunicipioOnlineSpider):
    TERRITORY_ID = "2800605"
    name = "se_barra_dos_coqueiros"
    start_date = date(2022, 9, 30)
    url_uf = "se"
    url_city = "barradoscoqueiros"
