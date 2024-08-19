from datetime import date

from gazette.spiders.base.portalgov import BasePortalGovSpider


class RjVarreSaiSpider(BasePortalGovSpider):
    name = "rj_varre_sai"
    TERRITORY_ID = "3306156"
    allowed_domains = ["varresai.rj.gov.br"]
    start_date = date(2019, 9, 21)
    power = "executive_legislative"
    domain = "varresai.rj.gov.br"
