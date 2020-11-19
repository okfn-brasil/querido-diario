from gazette.spiders.base import DoemGazetteSpider


class BaAcajutibaSpider(DoemGazetteSpider):
    TERRITORY_ID = "2900306"
    name = "ba_acajutiba"
    state_city_url_part = "ba/acajutiba"
