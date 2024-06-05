from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaDomBasilioSpider(SaiGazetteSpider):
    TERRITORY_ID = "2910107"
    name = "ba_dom_basilio"
    allowed_domains = ["dombasilio.ba.gov.br"]
    base_url = "https://www.dombasilio.ba.gov.br"
    start_date = date(2009, 1, 5)
