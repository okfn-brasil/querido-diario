from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class MgSapucaiMirimSpider(BaseDospSpider):
    TERRITORY_ID = "3165404"
    name = "mg_sapucai_mirim"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/sapucai_mirim"]
    start_date = date(2023, 11, 24)
