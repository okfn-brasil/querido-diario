from datetime import date

from gazette.spiders.base.barcodigital import BaseBarcoDigitalSpider


class ToLagoaDaConfusao(BaseBarcoDigitalSpider):
    name = "to_lagoa_da_confusao"
    TERRITORY_ID = "1711902"
    allowed_domains = ["api-lagoadac.barcodigital.com.br"]
    base_url = "https://api-lagoadac.barcodigital.com.br"

    start_date = date(2018, 11, 1)
