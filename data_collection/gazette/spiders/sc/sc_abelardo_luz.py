from datetime import date

from gazette.spiders.base.fecam import BaseFecamSpider


class ScAbelardoLuzSpider(BaseFecamSpider):
    name = "sc_abelardo_luz"
    PUBLIC_ENTITY_ID = "4200101"
    GAZETTES_PAGE_URL = (
        "https://www.diariomunicipal.sc.gov.br/?r=site/portal&codigoEntidade=5"
    )
    POWER = "executivo"
    start_date = date(2021, 5, 20)
