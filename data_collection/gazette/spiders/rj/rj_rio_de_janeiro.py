from datetime import date

from gazette.spiders.base.dionet import DionetGazetteSpider


class RjRioDeJaneiroSpider(DionetGazetteSpider):
    TERRITORY_ID = "3304557"
    name = "rj_rio_de_janeiro"
    allowed_domains = ["doweb.rio.rj.gov.br"]
    start_date = date(2006, 3, 16)

    BASE_URL = "https://doweb.rio.rj.gov.br"
