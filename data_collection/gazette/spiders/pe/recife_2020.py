import datetime as dt
import re

import scrapy
from chompjs import parse_js_object

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class PeRecifeSpider_2(BaseGazetteSpider):
    """Raspador para as publicações atuais de Recife (PE)

    Este raspador cobre o `sistema de publicações atual de Recife (PE)
    <https://dome.recife.pe.gov.br/dome/>`_ que publica desde 01/08/2020 até os dias
    atuais.

    Detalhes de implementação:
        O raspador utiliza um calendário na página inicial para listar em quais datas
        houveram publicações e realiza as requisições para as datas disponíveis. Cada
        data pode ter apenas uma publicação, que pode ser ordinária ou extraordinária,
        ou mais de uma publicação, contendo ambas.

    Exemplos:
        - `Publicação ordinária <https://dome.recife.pe.gov.br/dome/doDia.php?dataEdicao=2022-01-27>`_
        - `Publicação extraordinária <https://dome.recife.pe.gov.br/dome/doDia.php?dataEdicao=2022-01-28>`_
        - `Ambas publicações <https://dome.recife.pe.gov.br/dome/doDia.php?dataEdicao=2022-01-29>`_
    """

    name = "recife_2020"
    TERRITORY_ID = "2611606"

    start_date = dt.date(2020, 8, 2)
    allowed_domains = ["dome.recife.pe.gov.br"]
    BASE_URL = "https://dome.recife.pe.gov.br/dome/"
    start_urls = [BASE_URL]

    def parse(self, response):
        """Descobre datas disponíveis em calendário na página inicial e as requisita"""
        available_dates_js = re.search(
            r"var eventData = \[.+?\];", response.text, re.DOTALL
        ).group()
        available_dates = parse_js_object(available_dates_js)

        for date_metadata in available_dates:
            gazette_date = self._parse_date(date_metadata["date"])

            if not (self.start_date <= gazette_date <= self.end_date):
                continue

            callback = (
                self.parse_multi_publication_date
                if date_metadata["classname"] == "ambos"
                else self.parse_single_publication_date
            )
            yield scrapy.Request(
                url=f"{self.BASE_URL}doDia.php?dataEdicao={date_metadata['date']}",
                callback=callback,
                cb_kwargs={"date_metadata": date_metadata},
            )

    def parse_single_publication_date(self, response, date_metadata):
        """Raspa diário em data de publicação única"""
        iframe = response.css("div.pdf-box iframe")

        file_url = re.search(r"file=(.+?)&", iframe.attrib["src"]).group(1)
        is_extra_edition = (
            "extra" in file_url.lower() or date_metadata["classname"] == "extra"
        )

        yield self._build_item(
            title=date_metadata["title"],
            date=date_metadata["date"],
            file_url=file_url,
            is_extra_edition=is_extra_edition,
        )

    def parse_multi_publication_date(self, response, date_metadata):
        """Raspa diário em data com mais de um tipo de publicação"""
        publications = response.css("div.resultado a")

        for publication in publications:
            file_url = re.search(
                r"openPDF\('(.+?)'", publication.attrib["onclick"]
            ).group(1)
            is_extra_edition = (
                "extra" in publication.attrib["title"].lower() + file_url.lower()
            )

            yield self._build_item(
                title=publication.attrib["title"],
                date=date_metadata["date"],
                file_url=file_url,
                is_extra_edition=is_extra_edition,
            )

    def _parse_date(self, raw_date):
        """Transforma string de data em `datetime.date`"""
        return dt.datetime.strptime(raw_date, "%Y-%m-%d").date()

    def _build_item(self, title, date, file_url, is_extra_edition):
        """Deixa item `Gazette` pronto para ser salvo"""
        return Gazette(
            date=self._parse_date(date),
            file_urls=[file_url],
            edition_number=self._clean_zfill(
                re.search(r"Recife (\d+) Edição", title).group(1)
            ),
            is_extra_edition=is_extra_edition,
            power="executive_legislative",
        )

    def _clean_zfill(self, string_number):
        """Remove zeros à esquerda em string"""
        return string_number.lstrip("0")
