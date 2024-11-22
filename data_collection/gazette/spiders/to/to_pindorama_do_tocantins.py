from datetime import date

from gazette.spiders.base.barcodigital import BaseBarcoDigitalSpider


class ToPindoramaDoTocantins(BaseBarcoDigitalSpider):
    name = "to_pindorama_do_tocantins"
    TERRITORY_ID = "1717008"
    allowed_domains = ["api-pindorama.barcodigital.com.br"]
    base_url = "https://api-pindorama.barcodigital.com.br"

    start_date = date(year=2021, month=6, day=1)
