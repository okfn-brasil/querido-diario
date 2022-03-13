import datetime as dt
import re

import scrapy
from chompjs import parse_js_object
from dateutil.rrule import DAILY, rrule

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class PeRecifeSpiderAcervo2015A2020(BaseGazetteSpider):
    """Recife's (PE) spider for gazettes from 2015 to 2020

    This spider is implemented to crawl Recife's `gazette system
    <https://www.cepe.com.br/prefeituradiario/>`_ which covers gazettes from 30/04/2015
    to 01/08/2020. It uses an underlying API to do so.

    There is also a `deprecated system
    <http://www.recife.pe.gov.br/diariooficial-acervo/>`_ which covers gazettes from 2001
    to 2016 which is still not implemented.

    Implementation details:
        The spider generates all dates from the first available date (30/04/2015) until
        the last (01/08/2020). These dates are used to fetch the name of all available
        gazettes on that date, including Recife's. Then, the respective documents for
        Recife's gazettes are requested and the rest if filtered out.

    Gazettes examples:
        - http://200.238.105.211/cadernos/2020/20200326/8-PrefeituradoRecifeEdicaoExtra/PrefeituradoRecifeEdicaoExtra(20200326).pdf
        - http://200.238.105.211/cadernos/2020/20200613/8-PrefeituradoRecife/PrefeituradoRecife(20200613).pdf
        - http://200.238.105.211/cadernos/2020/20200616/8-PrefeituradoRecife/PrefeituradoRecife(20200616).pdf
    """

    name = "pe_recife_acervo_2015_a_2020"
    TERRITORY_ID = "2611606"

    start_date = dt.date(2015, 4, 30)
    end_date = dt.date(2020, 8, 1)
    allowed_domains = ["ws.cepe.com.br", "200.238.105.211"]
    EDITIONS_IN_DATE_URL = "https://ws.cepe.com.br/publicar/dows.php?&dia={full_date}"
    GAZETTE_URL = "http://200.238.105.211/cadernos/{full_year}/{full_date}/{edition_type}/{edition_type_name_only}({full_date}).pdf"

    def start_requests(self):
        """
        Requests documents which specifies edition types available for dates.
        """
        dates = rrule(freq=DAILY, dtstart=self.start_date, until=self.end_date)

        for date in dates:
            yield scrapy.Request(
                url=self.EDITIONS_IN_DATE_URL.format(full_date=date.strftime("%Y%m%d")),
                meta={"date": date.date()},
                callback=self.parse_editions_in_date,
            )

    def parse_editions_in_date(self, response):
        """
        Parses available editions to request only Recife's gazette documents.
        """
        recife_editions = self._find_recife_editions(response.text)
        date = response.meta["date"]

        for edition in recife_editions:
            url = self.GAZETTE_URL.format(
                full_year=date.strftime("%Y"),
                full_date=date.strftime("%Y%m%d"),
                edition_type=edition,
                edition_type_name_only=re.search(r"\w+$", edition).group(),
            )

            yield Gazette(
                date=date,
                file_urls=[url],
                is_extra_edition=self._is_extra(edition),
                power="executive_legislative",
            )

    def _find_recife_editions(self, text):
        """
        Finds editions related to Recife's gazette.

        Filters out entries which are not exclusively related to Recife
        (e.g. "1-PoderExecutivo").
        """
        return (
            edition
            for edition in text.split("&")
            if re.search("prefeituradorecife", edition, re.IGNORECASE)
        )

    def _is_extra(self, edition):
        """
        Checks if edition is extra or not.
        """
        return re.search("extra", edition, re.IGNORECASE) is not None


class PeRecifeSpider(BaseGazetteSpider):
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

    name = "pe_recife"
    TERRITORY_ID = "2611606"

    start_date = dt.date(2020, 8, 1)
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
