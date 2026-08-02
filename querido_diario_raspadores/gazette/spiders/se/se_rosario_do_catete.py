from datetime import date

from gazette.spiders.base.municipioonline import BaseMunicipioOnlineSpider


class SeRosarioDoCateteSpider(BaseMunicipioOnlineSpider):
    TERRITORY_ID = "2806107"
    name = "se_rosario_do_catete"
    url_uf = "se"
    url_city = "rosariodocatete"
    start_date = date(2021, 1, 12)
