import datetime
import re

import dateparser

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RsLajeadoSpider(BaseGazetteSpider):
    TERRITORY_ID = "4311403"

    name = "rs_lajeado"
    start_date = datetime.date(2016, 4, 5)

    user_agent = "curl/7.85.0"  # lol, idk. it works with curl
    start_urls = ["https://www.lajeado.rs.gov.br/conteudo/3718/1012"]

    def parse(self, response):
        pdfs = response.css(".accordion-card")

        # For some reason, there is a single entry that is duplicated in the website. So,
        # we save have a set of the entries already processed. We do this because the
        # spider will fail a SQL UNIQUE constraint when trying to insert repeated entries
        done = set()

        for item in pdfs:
            name = item.css(".accordion-card__conteudo::text").get()
            name = name.strip()

            href = item.css(".accordion-card__informacoes__baixar::attr(href)").get()
            href = href.strip()

            # Avoid reprocessing
            if name in done:
                continue

            # This file is missing
            if name == "23/03/20_edição_1000":
                continue

            done.add(name)

            yield Gazette(
                date=self.extract_date(name),
                edition_number=self.extract_edition(name),
                is_extra_edition=self.extract_is_extra_edition(name),
                file_urls=[href],
                power="executive",
                territory_id=self.TERRITORY_ID,
            )

    def extract_date(self, filename):
        filedate, *_ = filename.split("_")

        # There is a single case where the first day
        # of the month is represented like '1º'
        filedate = filedate.replace("º", "")
        filedate = dateparser.parse(filedate, languages=["pt"])
        return filedate.date()

    def extract_edition(self, filename):
        return re.search(r"edi[çc][aãâ][o0].+?(\d+)", filename, re.IGNORECASE).group(1)

    def extract_is_extra_edition(self, filename):
        """When there is no edition, the edition is extra"""
        return re.search(r"edi[çc][aãâ][o0].+?\d+$", filename, re.IGNORECASE) is None
