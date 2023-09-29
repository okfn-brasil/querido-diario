from datetime import date

from gazette.spiders.base.doem import DoemGazetteSpider


class SeNossaSenhoraDoSocorroSpider(DoemGazetteSpider):
    TERRITORY_ID = "2804805"
    name = "se_nossa_senhora_do_socorro"
    start_date = date(2022, 11, 7)  # edition_number 1
    state_city_url_part = "se/nossasenhoradosocorro"
