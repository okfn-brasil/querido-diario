from datetime import date

from gazette.spiders.base.doem import DoemGazetteSpider


class PrIpirangaSpider(DoemGazetteSpider):
    TERRITORY_ID = "4110508"
    name = "pr_ipiranga"
    state_city_url_part = "pr/ipiranga"
    start_date = date(2015, 9, 28)
