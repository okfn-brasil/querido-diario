from datetime import date

from gazette.spiders.base.barcodigital import BaseBarcoDigitalSpider


class ToTupiramaSpider(BaseBarcoDigitalSpider):
    name = "to_tupirama"
    TERRITORY_ID = "1721257"
    base_url = "https://api-tupirama.barcodigital.com.br"

    start_date = date(year=2017, month=1, day=1)
