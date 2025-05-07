from datetime import date

from gazette.spiders.base.imprensa_oficial import BaseImprensaOficialSpider


class BaSaoMiguelDasMatasSpider(BaseImprensaOficialSpider):
    name = "ba_sao_miguel_das_matas"
    start_date = date(2019, 2, 1)
    url_base = "http://saomigueldasmatas.ba.gov.br/{}"
    TERRITORY_ID = "2929404"
