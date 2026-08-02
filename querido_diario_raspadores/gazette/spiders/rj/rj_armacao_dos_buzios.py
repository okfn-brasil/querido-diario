from datetime import date

from gazette.spiders.base.adiarios_v2 import BaseAdiariosV2Spider


class RjArmacaoDosBuziosSpider(BaseAdiariosV2Spider):
    TERRITORY_ID = "3300233"
    name = "rj_armacao_dos_buzios"
    allowed_domains = ["buzios.aexecutivo.com.br"]
    BASE_URL = "https://buzios.aexecutivo.com.br"
    start_date = date(2015, 9, 3)
