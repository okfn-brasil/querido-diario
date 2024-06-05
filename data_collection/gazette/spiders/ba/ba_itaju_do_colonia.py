from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaItajuDoColoniaSpider(SaiGazetteSpider):
    TERRITORY_ID = "2915403"
    name = "ba_itaju_do_colonia"
    allowed_domains = ["itajudocolonia.ba.gov.br"]
    base_url = "https://www.itajudocolonia.ba.gov.br"
    start_date = date(2007, 1, 30)
