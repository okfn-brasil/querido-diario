import datetime as dt
import json
import re

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class PeCaruaruSpider(BaseGazetteSpider):
    name = "pe_caruaru"
    TERRITORY_ID = "2604106"
    allowed_domains = ["diariooficial.caruaru.pe.gov.br"]
    base_url = "https://diariooficial.caruaru.pe.gov.br"
    start_date = dt.date(2011, 12, 7)
    EDITION_NUMBER_REGEX = re.compile(r"\d+")

    async def start(self):
        # The date range search returns every edition of the period at once.
        yield scrapy.FormRequest(
            url=self.base_url,
            method="GET",
            formdata={
                "dataInicio": self.start_date.strftime("%d/%m/%Y"),
                "dataFim": self.end_date.strftime("%d/%m/%Y"),
            },
        )

    def parse(self, response):
        raw_editions = response.css("input#diariosJSON::attr(data-items)").get()
        if not raw_editions:
            self.logger.warning(f"Unable to find gazette data in {response.url}.")
            return

        # The website lists the newest edition first. Sorted the other way
        # around, the first occurrence of a repeated file is its oldest date.
        editions = json.loads(raw_editions)
        editions.sort(key=lambda edition: edition["dataEntrada"])

        gazettes = {}
        seen_urls = set()

        for edition in editions:
            gazette_date = dt.date.fromisoformat(edition["dataEntrada"])
            if not self.start_date <= gazette_date <= self.end_date:
                continue

            file_url = edition["arquivo"].get("url")
            if not file_url:
                self.logger.warning(f"Unable to find download URL for: {edition}.")
                continue

            file_url = response.urljoin(file_url)
            if file_url in seen_urls:
                continue
            seen_urls.add(file_url)

            edition_number = ""
            file_name = edition["arquivo"]["nome"]
            if number_match := self.EDITION_NUMBER_REGEX.search(file_name):
                edition_number = number_match.group().lstrip("0")

            # Editions published in parts (.part1, .part2...) are one gazette.
            gazettes.setdefault((gazette_date, edition_number), []).append(file_url)

        for (gazette_date, edition_number), file_urls in gazettes.items():
            yield Gazette(
                date=gazette_date,
                edition_number=edition_number,
                is_extra_edition=False,
                file_urls=file_urls,
                power="executive",
            )
