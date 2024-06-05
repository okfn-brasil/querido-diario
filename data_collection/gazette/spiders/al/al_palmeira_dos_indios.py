from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class AlPalmeiraDosIndiosSpider(SaiGazetteSpider):
    TERRITORY_ID = "2706307"
    name = "al_palmeira_dos_indios"
    allowed_domains = ["sai.io.org.br"]
    base_url = "https://sai.io.org.br/al/palmeiradosindios"
    start_date = date(2013, 12, 17)
