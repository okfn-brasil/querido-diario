import re
from datetime import datetime as dt

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class Base_RgSites(BaseGazetteSpider):
    def start_requests(self):
        start_urls = self.start_urls[0]
        yield scrapy.FormRequest(
            method="GET",
            url=start_urls,
        )

    def parse(self, response):
        self.end_date
        years = response.css(
            'div[role="tabpanel"]'
        )  # retorna vetor com os elementos separados por ano
        years.reverse()
        for year in years:
            ano = year.css("::attr(id)").get()
            ano = ano.replace("tab_", "")
            if int(ano) < self.start_date.year:
                continue
            months = year.css(
                "div.panel.panel-primary.rg-border-radius-none"
            )  # retorna vetor com os elementos separados por meses do ano selecionado
            for month in months:
                days = month.css("td.edicao")
                for day in days:
                    edicao = day.css('a[data-toggle="modal-pdf"]::text').get()
                    edicao = re.sub(r"\D", "", edicao)
                    url_pdf = day.css('a[data-toggle="modal-pdf"]::attr(href)').get()
                    data = day.css("span.visible-xs-inline-block::text").get()
                    data = (
                        data.strip()
                        .replace("\xa0", "")
                        .replace("(", "")
                        .replace(")", "")
                    )
                    data = dt.strptime(data, "%d/%m/%Y").date()
                    if (
                        int(ano) == self.start_date.year
                        and data.month < self.start_date.month
                    ):
                        break

                    if data < self.start_date:
                        continue

                    if data > self.end_date:
                        return
                    else:
                        yield Gazette(
                            date=data,  # dt.strptime(raw_gazette_date, "%d/%m/%Y").date()
                            edition_number=edicao,
                            is_extra_edition=False,
                            file_urls=[url_pdf],
                            power="executive",
                        )

        # Lógica de extração de metadados

        # partindo de response ...
        #
        # ... o que deve ser feito para coletar DATA DO DIÁRIO?
        # ... o que deve ser feito para coletar NÚMERO DA EDIÇÃO?
        # ... o que deve ser feito para coletar se a EDIÇÃO É EXTRA?
        # ... o que deve ser feito para coletar a URL DE DOWNLOAD do arquivo?
