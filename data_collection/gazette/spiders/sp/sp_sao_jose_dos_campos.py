from datetime import date

from gazette.spiders.base.dionet import DionetGazetteSpider


class SpSaoJoseDosCamposSpider(DionetGazetteSpider):
    TERRITORY_ID = "3549904"
    name = "sp_sao_jose_dos_campos"
    allowed_domains = ["diariodomunicipio.sjc.sp.gov.br"]
    start_date = date(2015, 8, 7)

    BASE_URL = "https://diariodomunicipio.sjc.sp.gov.br"
