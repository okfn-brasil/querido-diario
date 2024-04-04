from datetime import date

from gazette.spiders.base.imprensa_oficial import ImprensaOficialSpider


class BaConceicaoDoAlmeidaSpider(ImprensaOficialSpider):
    name = "ba_conceicao_do_almeida"
    allowed_domains = [
        "pmconceicaodoalmeidaba.imprensaoficial.org"
    ]  # https://www.conceicaodoalmeida.ba.gov.br/diario.html
    start_date = date(2019, 5, 1)
    city_domain = "http://conceicaodoalmeida.ba.gov.br"
    TERRITORY_ID = "2908309"
