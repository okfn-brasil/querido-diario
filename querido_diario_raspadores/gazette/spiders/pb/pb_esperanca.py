import datetime
import re

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class PbEsperancaSpider(BaseGazetteSpider):
    name = "pb_esperanca"
    TERRITORY_ID = "2506006"
    start_date = datetime.date(2017, 1, 1)
    start_urls = ["https://www.esperanca.pb.gov.br/publicacoes/quinzenarios"]
    allowed_domains = ["esperanca.pb.gov.br"]

    def parse(self, response):
        gazettes = response.xpath(
            "//a[contains(@href, '/publicacoes/quinzenarios/')"
            " and not(contains(@href, '?page='))]"
        )

        for gazette in gazettes:
            detail_url = gazette.xpath("./@href").get()
            raw_text = " ".join(gazette.xpath(".//text()").getall()).strip()
            if not detail_url or not raw_text:
                continue

            match_date = re.search(r"(\d{2})/(\d{2})/(\d{4})", raw_text)
            if not match_date:
                continue

            gazette_date = datetime.datetime.strptime(
                match_date.group(0), "%d/%m/%Y"
            ).date()

            if gazette_date > self.end_date:
                continue
            elif gazette_date < self.start_date:
                return

            raw_lower = raw_text.lower()
            terms = ["extra", "suplemento", "especial"]
            is_extra = any(term in raw_lower for term in terms)

            match_edition = re.search(
                r"(?:edição|n[ºo°]?|"
                r"quinzenário oficial de esperança n[ºo°]?)\s*(\d+)",
                raw_text,
                re.IGNORECASE,
            )
            edition_number = match_edition.group(1) if match_edition else ""

            yield response.follow(
                detail_url,
                callback=self.parse_gazette,
                cb_kwargs={
                    "gazette_date": gazette_date,
                    "edition_number": edition_number,
                    "is_extra_edition": is_extra,
                },
            )

        next_page = (
            response.xpath(
                "//a[contains(@href, '?page=') and contains(., 'Próximo')]/@href"
            ).get()
            or response.xpath("//a[@rel='next']/@href").get()
        )
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_gazette(
        self,
        response,
        gazette_date,
        edition_number,
        is_extra_edition,
    ):
        pdf_url = response.xpath("//a[contains(@href, '.pdf')]/@href").get()
        if pdf_url:
            yield Gazette(
                date=gazette_date,
                edition_number=edition_number,
                is_extra_edition=is_extra_edition,
                power="executive",
                file_urls=[response.urljoin(pdf_url)],
            )
