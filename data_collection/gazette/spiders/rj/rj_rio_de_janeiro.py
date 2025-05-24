from datetime import date

from gazette.spiders.base.dionet import BaseDionetSpider


class RjRioDeJaneiroSpider(BaseDionetSpider):
    TERRITORY_ID = "3304557"
    name = "rj_rio_de_janeiro"
    start_date = date(2006, 3, 16)

    BASE_URL = "https://doweb.rio.rj.gov.br"
