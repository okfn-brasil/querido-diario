import re
import datetime
from urllib.parse import urlencode
from dateutil.rrule import rrule, MONTHLY

import scrapy
import dateparser

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class CeCaucaia(BaseGazetteSpider):
    TERRITORY_ID = "2303709"

    name = "ce_caucaia"
    allowed_domains = ["caucaia.ce.gov.br"]
    start_date = datetime.date(2002, 6, 3)

    BASE_URL = "http://www.caucaia.ce.gov.br"
    params = {"tabela": "pagina", "acao": "diario_buscar_data"}
    FROM_URL = f"{BASE_URL}/index.php?{urlencode(params)}"

    month_number_to_name = {
        1: "Janeiro",
        2: "Fevereiro",
        3: "Março",
        4: "Abril",
        5: "Maio",
        6: "Junho",
        7: "Julho",
        8: "Agosto",
        9: "Setembro",
        10: "Outubro",
        11: "Novembro",
        12: "Dezembro",
    }

    def start_requests(self):
        rule_start_date = datetime.date(self.start_date.year, self.start_date.month, 1)

        date_list = list(
            rrule(freq=MONTHLY, dtstart=rule_start_date, until=datetime.date.today())
        )
        for date in date_list:
            formdata = {
                "pesquisa_data_mes": self.month_number_to_name.get(date.month),
                "pesquisa_data_ano": str(date.year),
            }
            yield scrapy.FormRequest(
                url=self.FROM_URL, method="POST", formdata=formdata
            )

    def parse(self, response):
        for document in response.css(".col-md-12 div:nth-child(2) div"):
            for document_link in document.css(".link-noticia"):
                file_url_sufix = document_link.css("::attr(href)").get()
                file_url = f"{self.BASE_URL}{file_url_sufix}"

                text = " ".join(document.css("*::text").getall())
                text = re.sub(r"\s+", " ", text).strip()

                date_text = re.search(r"\d{2}\/\d{2}\/\d{2}", text).group(0)
                date = datetime.datetime.strptime(date_text, "%d/%m/%y").date()
                edition_number = re.search(r"\d{4}\/(\d+)", text).group(1)

                is_extra_edition = bool(
                    re.search(r"suplementar|complementar", text, re.IGNORECASE)
                )

                yield Gazette(
                    date=date,
                    file_urls=[file_url],
                    is_extra_edition=is_extra_edition,
                    power="executive_legislative",
                    edition_number=edition_number,
                )
