import re
from datetime import date

import dateparser
import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RnMacaibaSpider(BaseGazetteSpider):
    """
    A listagem de diários é paginada e ordenada da edição mais recente para a
    mais antiga. O filtro por data do site não é usado porque, com ele, os links
    dos resultados deixam de apontar para os arquivos PDF.
    """

    TERRITORY_ID = "2407104"
    name = "rn_macaiba"
    allowed_domains = ["macaiba.rn.gov.br"]
    start_urls = ["https://macaiba.rn.gov.br/servicos/diario-oficial/"]
    start_date = date(2013, 8, 9)

    def parse(self, response):
        listed_dates = []

        for gazette in response.css("li.link_item a"):
            title = " ".join(gazette.css("::text").get().split())
            raw_edition, raw_date = title.rsplit(" - ", 1)
            listed_date = dateparser.parse(
                raw_date.replace("/", " de "), languages=["pt"]
            ).date()
            listed_dates.append(listed_date)

            file_url = gazette.attrib["href"]
            gazette_date = self._fix_year(listed_date, file_url)
            if not self.start_date <= gazette_date <= self.end_date:
                continue

            yield Gazette(
                date=gazette_date,
                edition_number=re.search(r"\d+", raw_edition).group().lstrip("0"),
                is_extra_edition="extra" in raw_edition.lower(),
                file_urls=[file_url],
                power="executive_legislative",
            )

        # Como a listagem é decrescente, a próxima página só pode ter edições do
        # intervalo enquanto a edição mais antiga desta página não for anterior
        # a start_date. Um mesmo dia pode ter edições em páginas diferentes.
        if listed_dates and min(listed_dates) >= self.start_date:
            next_page_url = response.css("a.nextpostslink::attr(href)").get()
            if next_page_url:
                yield scrapy.Request(next_page_url)

    def _fix_year(self, listed_date, file_url):
        # Algumas edições aparecem na listagem com o ano errado (ex.: DOMM 0143,
        # de 19/12/2018, listada como 19/12/2019). Os arquivos do site antigo
        # trazem a data da edição no caminho, que prevalece nesses casos
        url_date = re.search(r"/boletins/(\d{4})/(\d{2})/(\d{2})/", file_url)
        if url_date is None:
            return listed_date

        year, month, day = (int(value) for value in url_date.groups())
        if (month, day) == (listed_date.month, listed_date.day):
            return listed_date.replace(year=year)
        return listed_date
