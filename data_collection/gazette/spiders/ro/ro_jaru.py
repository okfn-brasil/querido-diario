from datetime import date

from gazette.spiders.base.dionet import DionetGazetteSpider


class RoJaruSpider(DionetGazetteSpider):
    TERRITORY_ID = "1100114"
    name = "ro_jaru"
    allowed_domains = ["doe.jaru.ro.gov.br"]
    start_date = date(2022, 1, 1)

    BASE_URL = "https://doe.jaru.ro.gov.br"
