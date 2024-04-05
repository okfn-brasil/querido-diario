from datetime import date

from gazette.spiders.base.imprensa_oficial import ImprensaOficialSpider


class BaSaoMiguelDasMatasSpider(ImprensaOficialSpider):
    name = "ba_sao_miguel_das_matas"
    allowed_domains = ["pmsaomigueldasmatasba.imprensaoficial.org"]
    start_date = date(2019, 2, 1)
    city_domain = "http://pmsaomigueldasmatasba.imprensaoficial.org"
    TERRITORY_ID = "2929404"
