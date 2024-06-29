from datetime import date

from gazette.spiders.base.imprensa_oficial import ImprensaOficialSpider


class BaSapeacuSpider(ImprensaOficialSpider):
    name = "ba_sapeacu"
    allowed_domains = ["pmsapeacuba.imprensaoficial.org"]
    start_date = date(2017, 1, 1)
    city_domain = "http://pmsapeacuba.imprensaoficial.org"
    TERRITORY_ID = "2929602"
