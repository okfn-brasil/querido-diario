from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class MgOncaDePitanguiSpider(BaseInstarSpider):
    TERRITORY_ID = "3145802"
    name = "mg_onca_de_pitangui"
    allowed_domains = ["oncadopitangui.mg.gov.br"]
    base_url = "https://www.oncadopitangui.mg.gov.br/portal/diario-oficial"
    start_date = date(2021, 5, 24)
