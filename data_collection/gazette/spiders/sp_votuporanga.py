from base64 import b64encode
from datetime import date, datetime
from json import loads

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class SpVotuporangaSpider(BaseGazetteSpider):

    """
    Raspador para as Publicaçoes dos Diarios Oficiais de Votuporanga.
    Atualmente Publicando: https://www.imprensaoficialmunicipal.com.br/votuporanga.
    Porém, foi encontrado link da API para JSON
    """

    TERRITORY_ID = "3557105"
    name = "sp_votuporanga"
    allowed_domains = ["dosp.com.br"]
    start_urls = ["https://dosp.com.br/api/index.php/dioe.js/5292"]
    start_date = date(2015, 10, 5)
    end_date = datetime.today().date()

    def parse(self, response):
        json_text = (
            response.css("p::text").get().replace("parseResponse(", "")
        ).replace(");", "")

        json_text = loads(json_text)

        for diarios in json_text["data"]:
            data = datetime.strptime(diarios["data"], "%Y-%m-%d").date()
            link = b64encode(bytearray(str(diarios["iddo"]), "utf-8")).decode("utf-8")

            if self.start_date <= data <= self.end_date:
                yield Gazette(
                    date=data,
                    edition_number=diarios["edicao_do"],
                    file_urls=[
                        f"https://dosp.com.br/exibe_do.php?i={link}.pdf",
                    ],
                    is_extra_edition=diarios["flag_extra"] > 0,
                    power="executive",
                )
