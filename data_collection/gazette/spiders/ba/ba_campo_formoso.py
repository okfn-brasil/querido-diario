from datetime import date

from gazette.spiders.base.doem import DoemGazetteSpider


class BaCampoFormosoSpider(DoemGazetteSpider):
    TERRITORY_ID = "2906006"
    name = "ba_campo_formoso"
    state_city_url_part = "ba/campoformoso"
    start_date = date(2013, 1, 31)
