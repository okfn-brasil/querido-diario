from datetime import date

from gazette.spiders.base.municipioonline import BaseMunicipioOnlineSpider


class SeBarraDosCoqueirosSpider(BaseMunicipioOnlineSpider):
    TERRITORY_ID = "2800605"
    name = "se_barra_dos_coqueiros"
    url_uf = "se"
    url_city = "barradoscoqueiros"
    start_date = date(2022, 9, 30)
