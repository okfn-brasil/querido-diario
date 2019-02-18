# from dateparser import parse
import datetime as dt

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


# Lista de todas as datas contendo diário (2017-2019):
# https://www.cepe.com.br/prefeituradiario/diarios.txt

# URL pra acessar um diário:
# http://200.238.101.22/docreader/docreader.aspx?bib=R20160324&pasta=Marco\Dia%2024


class PeRecifeSpider(BaseGazetteSpider):
    MUNICIPALITY_ID = ""
    name = "pe_recife"
    allowed_domains = ["cepe.com.br", "200.238.101.22"]

    month_dict = {
        "01": "Janeiro",
        "02": "Fevereiro",
        "03": "Marco",
        "04": "Abril",
        "05": "Maio",
        "06": "Junho",
        "07": "Julho",
        "08": "Agosto",
        "09": "Setembro",
        "10": "Outubro",
        "11": "Novembro",
        "12": "Dezembro",
    }

    BASE_URL = (
        "http://200.238.101.22/docreader/docreader.aspx?"
        "bib={bib_code}&pasta={pasta_code}"
    )

    DOWNLOAD_URL = (
        "http://200.238.101.22/docreader/saveasfile.aspx?"
        "cache=cache/{doc_id}&arq=Arquivo.pdf"
    )

    def start_requests(self):
        current_date = dt.date.today()
        day_comp = int(dt.datetime.strftime(current_date, "%Y%m%d"))
        return self.make_document_request(current_date, day_comp)

    def make_document_request(self, current_date, day_comp):
        # TODO: fix for loop
        for day_int in range(day_comp, 20_150_430, -1):
            current_month = current_date.month
            month_str = self.month_dict[f"{current_month:0>2}"]
            day_str = f"{current_date.day:0>2}"
            bib_code = f"R{day_int}"
            pasta_code = f"{month_str}\\Dia%20{day_str}"
            url = self.BASE_URL.format(bib_code=bib_code, pasta_code=pasta_code)

            doc_date = current_date
            current_date = dt.datetime.strptime(str(day_int), "%Y%m%d")
            # next date
            # current_date = current_date - dt.timedelta(days=1)
            # day_comp = int(dt.datetime.strftime(current_date, "%Y%m%d"))

            yield scrapy.Request(url, self.parse_document, meta={"date": doc_date})

    def parse_document(self, response):
        hidden_id = response.css("input[id=HiddenID]::attr(value)").extract_first()
        items = []
        if hidden_id:
            url = self.DOWNLOAD_URL.format(doc_id=hidden_id)
            items.append(
                Gazette(
                    date=response.meta["date"],
                    file_urls=[url],
                    territory_id=self.MUNICIPALITY_ID,
                    scraped_at=dt.datetime.utcnow(),
                )
            )
        return items
