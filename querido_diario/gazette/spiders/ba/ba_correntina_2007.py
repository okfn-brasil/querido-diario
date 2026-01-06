from datetime import date

from gazette.spiders.base.diof import BaseDiofSpider


class BaCorrentinaSpider(BaseDiofSpider):
    TERRITORY_ID = "2909307"
    name = "ba_correntina_2007"
    website = (
        "https://dom.imap.org.br/sitesMunicipios/imprensaOficial.cfm?varCodigo=219"
    )
    power = "executive"
    start_date = date(2007, 11, 30)
    end_date = date(2024, 12, 31)
