from gazette.spiders.base.instar import BaseInstarSpider


class MgContagemSpider(BaseInstarSpider):
    TERRITORY_ID = "3118601"
    name = "mg_contagem"
    allowed_domains = ["contagem.mg.gov.br"]
    base_url = "https://www.portal.contagem.mg.gov.br/portal/diario-oficial"
