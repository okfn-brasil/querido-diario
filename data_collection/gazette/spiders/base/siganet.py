import datetime

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class SiganetSpider(BaseGazetteSpider):
    def parse(self, response):
        sorted_json = sorted(response.json()["data"], key=lambda x: datetime.datetime.strptime(x["TDI_DT_PUBLICACAO"], "%Y-%m-%d %H:%M:%S").date())
        for gazette in sorted_json:
            gazette_date = datetime.datetime.strptime(
                gazette["TDI_DT_PUBLICACAO"], "%Y-%m-%d %H:%M:%S"
            ).date()

            if self.end_date < gazette_date:
                break
            if self.start_date > gazette_date:
                continue
            
            if int(gazette["TDI_TPS_ID"]) == 2:
                pdf_url = f"https://painel.siganet.net.br/upload/000000000{gazette['TDI_TPS_ID']}/cms/publicacoes/diario/{gazette['TDI_ARQUIVO']}"
            else:
                pdf_url = f"https://painel.siganet.net.br/upload/0000000{gazette['TDI_TPS_ID']}/cms/publicacoes/diario/{gazette['TDI_ARQUIVO']}"

            yield Gazette(
                date=gazette_date,
                file_urls=[pdf_url],
                is_extra_edition=False,
                edition_number=gazette["TDI_EDICAO"],
                power="executive",
            )