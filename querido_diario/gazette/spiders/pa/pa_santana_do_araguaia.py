import datetime

from gazette.spiders.base.adminlte import BaseAdminLteSpider


class PaSantanaDoAraguaiaSpider(BaseAdminLteSpider):
    TERRITORY_ID = "1506708"
    name = "pa_santana_do_araguaia"
    allowed_domains = ["diariooficial.pmsaraguaia.pa.gov.br"]
    start_date = datetime.date(2022, 2, 11)
    city_domain = "pmsaraguaia.pa.gov.br"
