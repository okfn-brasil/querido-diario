from gazette.spiders.base.instar import BaseInstarSpider

class MgContagemSpider(BaseInstarSpider):
    TERRITORY_ID = "3547809"
    name = "sp_santo_andre"
    allowed_domains = ["santoandre.sp.gov.br"]
    base_url = "https://web.santoandre.sp.gov.br/portal/diario-oficial"