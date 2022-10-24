from datetime import date

from gazette.spiders.base.siganet import SiganetSpider


class MaSantaLuziaDoParuaSpider(SiganetSpider):

    name = "ma_santa_luzia_do_parua"
    allowed_domains = ["transparencia.santaluziadoparua.ma.gov.br"]
    start_date = date(2018, 8, 18)
    url_base = "https://transparencia.santaluziadoparua.ma.gov.br/acessoInformacao/diario/diario/listarDiario"
    TERRITORY_ID = "2110039"