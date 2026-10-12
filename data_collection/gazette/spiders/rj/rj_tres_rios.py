import re
from datetime import date, datetime as dt

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RjTresRiosSpider(BaseGazetteSpider):
    name = "rj_tres_rios"
    TERRITORY_ID = "3306008"
    allowed_domains = ["tresrios.rj.gov.br"]
    start_urls = ["https://tresrios.rj.gov.br/bio"]
    start_date = date(2018, 1, 10)

    def parse(self, response):
        years = response.css("div.wgl-accordion_panel div.wgl-accordion_content")
        for year in years:
            for item in year.css("p"):
                full_text = "".join(item.css("::text").getall())
                full_text = full_text.replace("/", "-").replace(".", "-")

                gazette_pattern = (
                    r"^Boletim Informativo.* (\d{4,}).* (\d{2}-\d{2}-\d{4})"
                )
                match = re.match(gazette_pattern, full_text)
                if not match:
                    continue

                temp_date = dt.strptime(match.group(2), "%d-%m-%Y").date()
                if temp_date > self.end_date:
                    continue
                if temp_date < self.start_date:
                    return

                num_ed = match.group(1)
                extra_ed = bool(re.search(r"extra|supl", full_text, re.IGNORECASE))

                # Em algumas edições há mais de um link na descrição da edição e apenas um dos links aponta para a edição correta. Ex. Edição de 16/01/2025
                # Em outros casos não o número da edição no link. Ex. Edição de 15/01/2021

                links = item.xpath(".//a/@href")
                if len(links) == 1:
                    url = links.get()
                else:
                    url = item.xpath(f"//a[contains(@href, '{num_ed}')]/@href").get()

                yield Gazette(
                    date=temp_date,
                    edition_number=num_ed,
                    is_extra_edition=extra_ed,
                    file_urls=[url],
                    power="executive",
                )
