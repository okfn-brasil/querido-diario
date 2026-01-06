import datetime

from gazette.spiders.base.adminlte import BaseAdminLteSpider


class ToGurupiSpider(BaseAdminLteSpider):
    TERRITORY_ID = "1709500"
    name = "to_gurupi"
    allowed_domains = ["diariooficial.gurupi.to.gov.br"]
    start_date = datetime.date(2020, 5, 28)
    city_domain = "gurupi.to.gov.br"
