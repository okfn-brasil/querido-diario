from datetime import date

from gazette.spiders.base.barcodigital import BaseBarcoDigitalSpider


class ToRecursolandiaSpider(BaseBarcoDigitalSpider):
    name = "to_recursolandia"
    TERRITORY_ID = "1718501"
    base_url = "https://api-recursolandia.barcodigital.com.br"

    start_date = date(year=2019, month=11, day=11)
