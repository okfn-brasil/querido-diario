from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class MgMonsenhorPauloSpider(BaseDospSpider):
    TERRITORY_ID = "3142601"
    name = "mg_monsenhor_paulo"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/monsenhor_paulo"]
    start_date = date(2017, 4, 12)
