from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpSantaRitaDoPassaQuatroSpider(BaseDospSpider):
    TERRITORY_ID = "3547502"
    name = "sp_santa_rita_do_passa_quatro"
    start_urls = [
        "https://www.imprensaoficialmunicipal.com.br/santa_rita_do_passa_quatro"
    ]
    start_date = date(2018, 1, 8)

    def parse_json(self, response):
        # O diário também publica atos da Câmara Municipal
        for gazette in super().parse_json(response):
            gazette["power"] = "executive_legislative"
            yield gazette
