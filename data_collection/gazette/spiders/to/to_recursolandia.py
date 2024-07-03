from datetime import date

from gazette.spiders.base.barcodigital import BarcoDigitalSpider


class ToRecursolandiaSpider(BarcoDigitalSpider):
    name = "to_recursolandia"
    TERRITORY_ID = "1718501"
    allowed_domains = ["api-recursolandia.barcodigital.com.br"]
    base_url = "https://api-recursolandia.barcodigital.com.br"

    start_date = date(year=2019, month=11, day=11)
