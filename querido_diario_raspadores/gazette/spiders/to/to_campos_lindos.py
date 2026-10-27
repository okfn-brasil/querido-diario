from datetime import date

from gazette.spiders.base.govweb import BaseGovWebSpider


class ToCamposLindosSpider(BaseGovWebSpider):
    TERRITORY_ID = "1703842"
    name = "to_campos_lindos"
    base_url = "https://www.camposlindos.to.gov.br"
    start_date = date(2021, 5, 31)
