from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class PbCachoeiraDosIndiosSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2503308"
    name = "pb_cachoeira_dos_indios"
    allowed_domains = ["cachoeiradosindios.pb.gov.br"]
    BASE_URL = "https://www.cachoeiradosindios.pb.gov.br"
    start_date = date(202, 8, 23)
