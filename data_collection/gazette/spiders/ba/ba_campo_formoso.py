from datetime import date

from gazette.spiders.base.doem import DoemGazetteSpider


class BaCampoFormosoSpider(DoemGazetteSpider):
    TERRITORY_ID = "2906006"
    name = "ba_campo_formoso"
    start_date = date(2018, 1, 3)  # edition_number 873
    state_city_url_part = "ba/campoformoso"
