from datetime import date

from gazette.spiders.base.diariomunicipal import BaseDiarioMunicipalSpider


class ScAbdonBatistaSpider(BaseDiarioMunicipalSpider):
    name = "sc_abdon_batista"
    PUBLIC_ENTITY_ID = "4200051"
    GAZETTES_PAGE_URL = (
        "https://www.diariomunicipal.sc.gov.br/?r=site/portal&codigoEntidade=4"
    )
    POWER = "executivo"
    start_date = date(2014, 7, 30)
