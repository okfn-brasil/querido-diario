from datetime import date
from re import findall

import dateparser
from scrapy.selector import Selector

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class PrGuaratubaSpider(BaseGazetteSpider):
    name = "pr_guaratuba"
    TERRITORY_ID = "4109609"
    allowed_domains = ["portal.guaratuba.pr.gov.br"]
    start_urls = ["http://portal.guaratuba.pr.gov.br/diariosoficiais"]
    start_date = date(2010, 1, 1)
    base_url = "http://portal.guaratuba.pr.gov.br/"

    def _parse_edition_number(self, text):
        matches = (
            findall(r"edição \w+\d+", text.lower())
            + findall(r"edição \w+ \w+\d+", text.lower())
            + findall(r"\d+/\d+", text.lower())
        )
        if len(matches) > 0:
            edition_number = findall(r"\d+/\d+", matches[0]) + findall(
                r"\d+", matches[0]
            )
            if len(edition_number) > 0:
                return "".join(edition_number[0].split("/")[-1::-1])
        return ""

    def _extract_label_edition_number(self, link_selector):
        img = link_selector.css("*>*").get()
        label = link_selector.get().strip().replace(img, "")
        label = Selector(text=label).css("::text")
        _edition_number = self._parse_edition_number(label.get())
        label = label.get().strip()
        return label, _edition_number

    def parse(self, response):
        map_date_edition = dict()
        for line in response.css(".table.table-striped tr"):
            td_selector = line.css("td")
            if (
                len(td_selector) == 0
                or td_selector.get()
                and td_selector.get().find("Data da Publicação") != -1
            ):
                continue
            else:
                _gazzete_date = dateparser.parse(
                    line.css("td p::text").get(), languages=["pt"]
                )
                gazzete_date = _gazzete_date.date()
                pdf_links = []
                edition_number, is_extra_edition = None, False
                for link_selector in line.css("td")[1].css("a"):
                    pdf_relative_link = link_selector.css("::attr(href)").get()
                    pdf_links.append(self.base_url + pdf_relative_link)

                    label = link_selector.css("::text").get().strip()

                    if not label:
                        label, _edition_number = self._extract_label_edition_number(
                            link_selector
                        )
                    else:
                        _edition_number = self._parse_edition_number(label)

                    if edition_number is None:
                        date_key = _gazzete_date.strftime("%Y-%m-%d")
                        if date_key not in map_date_edition:
                            edition_number = _edition_number
                            map_date_edition[date_key] = _edition_number
                        else:
                            edition_number = map_date_edition[date_key]

                        is_extra_edition = "extra" in label.lower()

                if self.start_date <= gazzete_date <= self.end_date:
                    yield Gazette(
                        date=gazzete_date,
                        edition_number=edition_number,
                        is_extra_edition=is_extra_edition,
                        file_urls=pdf_links,
                        power="executive",
                    )
