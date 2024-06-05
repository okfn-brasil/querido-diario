from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaSitioDoQuintoSpider(SaiGazetteSpider):
    TERRITORY_ID = "2930766"
    name = "ba_sitio_do_quinto"
    allowed_domains = ["sitiodoquinto.ba.gov.br"]
    base_url = "https://www.sitiodoquinto.ba.gov.br"
    start_date = date(2007, 8, 22)
