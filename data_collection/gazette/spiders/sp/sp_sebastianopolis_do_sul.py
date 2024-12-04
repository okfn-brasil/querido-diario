from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpSebastianopolisDoSulSpider(BaseInstarSpider):
    TERRITORY_ID = "3551306"
    name = "sp_sebastianopolis_do_sul"
    allowed_domains = ["sebastianopolisdosul.sp.gov.br"]
    base_url = "https://www.sebastianopolisdosul.sp.gov.br/portal/diario-oficial"
    start_date = date(2020, 5, 26)
