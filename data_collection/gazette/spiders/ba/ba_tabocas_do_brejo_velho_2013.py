from datetime import date

from gazette.spiders.base.doem import DoemGazetteSpider


class BaTabocasDoBrejoVelhoSpider(DoemGazetteSpider):
    TERRITORY_ID = "2930907"
    name = "ba_tabocas_do_brejo_velho_2013"
    state_city_url_part = "ba/tabocasdobrejovelho"
    start_date = date(2013, 1, 4)
