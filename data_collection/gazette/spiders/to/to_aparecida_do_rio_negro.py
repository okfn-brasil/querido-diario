from datetime import date

from gazette.spiders.base.barcodigital import BaseBarcoDigitalSpider


class ToAparecidaDoRioNegro(BaseBarcoDigitalSpider):
    name = "to_aparecida_do_rio_negro"
    TERRITORY_ID = "1701101"
    allowed_domains = ["api-pmaparecida.barcodigital.com.br"]
    base_url = "https://api-pmaparecida.barcodigital.com.br"

    start_date = date(2017, 7, 13)
