import datetime as dt

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RjSaoJoaoDeMeritiSpider(BaseGazetteSpider):
    TERRITORY_ID = "3305109"
    name = "rj_sao_joao_de_meriti"
    allowed_domains = ["transparencia.meriti.rj.gov.br"]
    start_urls = ["https://transparencia.meriti.rj.gov.br/diario_oficial_get.php"]
    BASE_URL = "https://transparencia.meriti.rj.gov.br/ver20230623/WEB-ObterAnexo.rule?sys=LAI&codigo="
    start_date = dt.date(2017, 1, 1)
    custom_settings = {"DOWNLOAD_DELAY": 0.5, "RANDOMIZE_DOWNLOAD_DELAY": True}

    def parse(self, response):
        for gazette_data in response.json():
            raw_gazette_date = gazette_data["Data_Formatada"]
            gazette_date = dt.datetime.strptime(raw_gazette_date, "%d/%m/%Y").date()

            if not self.start_date <= gazette_date <= self.end_date:
                continue
            gazette_code = gazette_data["Codigo_ANEXO"]
            # links quebrados no portal de transparência
            if gazette_code == 1:
                continue
            gazette_edition_number = gazette_data["ANEXO"]
            gazette_url = f"{self.BASE_URL}{gazette_code}"

            yield Gazette(
                date=gazette_date,
                edition_number=gazette_edition_number,
                file_urls=[gazette_url],
                is_extra_edition=False,
                power="executive_legislative",
            )
