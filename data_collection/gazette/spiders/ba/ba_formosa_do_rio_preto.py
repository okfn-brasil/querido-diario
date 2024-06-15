from datetime import date

from gazette.spiders.base.doem import DoemGazetteSpider


class BaFormosaDoRioPretoSpider(DoemGazetteSpider):
    TERRITORY_ID = "2911105"
    name = "ba_formosa_do_rio_preto"
    state_city_url_part = "ba/formosadoriopreto"
    start_date = date(2021, 1, 4)
