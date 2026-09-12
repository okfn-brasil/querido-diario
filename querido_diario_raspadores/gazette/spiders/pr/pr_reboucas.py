from datetime import date

from gazette.spiders.base.ptio import BasePtioSpider


class PrReboucasSpider(BasePtioSpider):
    name = "pr_reboucas"
    TERRITORY_ID = "4121505"
    BASE_URL = "http://pr.portaldatransparencia.com.br/prefeitura/reboucas/"
    start_date = date(2010, 12, 1)
