from datetime import date

from gazette.spiders.base.diariomunicipal import BaseDiarioMunicipalSpider


class ScFlorianopolisSpider(BaseDiarioMunicipalSpider):
    name = "sc_florianopolis_2024"
    PUBLIC_ENTITY_ID = "4205407"
    GAZETTES_PAGE_URL = (
        "https://www.diariomunicipal.sc.gov.br/?r=site/portal&codigoEntidade=92"
    )
    POWER = "executivo"
    start_date = date(2024, 8, 5)
