from datetime import date

from gazette.spiders.base.siganet import SiganetSpider


class MaBacuritubaSpider(SiganetSpider):

    name = "ma_bacurituba"
    allowed_domains = ["transparencia.bacurituba.ma.gov.br"]
    start_date = date(2018, 4, 6)
    url_base = "https://transparencia.bacurituba.ma.gov.br/acessoInformacao/diario/diario/listarDiario"
    TERRITORY_ID = "2101350"