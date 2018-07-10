from gazette.items import Gazette
import datetime as dt
import re
import scrapy
from gazette.spiders.base import BaseGazetteSpider


class RjRioDeJaneiroSpider(BaseGazetteSpider):
    TERRITORY_ID = "3304557"
    name = "rj_rio_de_janeiro"
    allowed_domains = ["doweb.rio.rj.gov.br"]
    start_urls = ["http://doweb.rio.rj.gov.br"]
    search_gazette_url = (
        "http://doweb.rio.rj.gov.br/?buscar_diario=ok&tipo=1&data_busca={}"
    )  # format 20/04/2018
    download_gazette_url = (
        "http://doweb.rio.rj.gov.br/ler_pdf.php?download=ok&edi_id={}"
    )  # 20/04/2018 has edi_id = 3734

    def parse(self, response):
        parsing_date = dt.date.today()
        end_date = dt.date(2015, 1, 1)
        while parsing_date >= end_date:
            url = self.search_gazette_url.format(parsing_date.strftime("%d/%m/%Y"))
            yield scrapy.Request(
                url, self.parse_search_by_date, meta={"gazette_date": parsing_date}
            )

            parsing_date = parsing_date - dt.timedelta(days=1)

    def parse_search_by_date(self, response):
        gazette_date = response.meta.get("gazette_date")

        no_gazettes = response.css("#dialog-message").extract_first()
        if no_gazettes and "Não existe publicação para esta data" in no_gazettes:
            return

        items = []
        one_gazette = response.css(
            "#conteudo_principal > #conteudo_home > #conteudo_erro script"
        ).extract_first()
        if one_gazette:
            match = re.search(".*edi_id=([0-9]+).*", one_gazette)
            if match:
                url = self.download_gazette_url.format(match.group(1))
                items.append(self.create_gazette(gazette_date, url))

        multiple_gazettes = response.css("#dialog-message").extract_first()
        if (
            multiple_gazettes
            and "Existe mais de uma publicação para esta data" in multiple_gazettes
        ):
            editions = response.css("#dialog-message a").extract()
            for ed in editions:
                match = re.search(".*edi_id=([0-9]+).*", ed)
                if match:
                    url = self.download_gazette_url.format(match.group(1))
                    is_extra_edition = "suplemento" in ed.lower()
                    items.append(
                        self.create_gazette(gazette_date, url, is_extra_edition)
                    )

        return items

    def create_gazette(self, date, url, is_extra_edition=False):
        return Gazette(
            date=date,
            file_urls=[url],
            is_extra_edition=is_extra_edition,
            territory_id=self.TERRITORY_ID,
            power="executive",
            scraped_at=dt.datetime.utcnow(),
        )
