from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpMogiGuacuSpider(BaseDospSpider):
    TERRITORY_ID = "3530706"
    name = "sp_mogi_guacu"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/mogi_guacu"]
    start_date = date(2022, 1, 20)
