from datetime import date

from gazette.spiders.base.doem import DoemGazetteSpider


class BaCampoAlegreDeLourdesSpider(DoemGazetteSpider):
    TERRITORY_ID = "2905909"
    name = "ba_campo_alegre_de_lourdes"
    start_date = date(2020, 11, 30)  # Primeira edição em 30/11/2020
    state_city_url_part = "ba/campoalegredelourdes"
