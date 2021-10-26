import json
import re
from datetime import date

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class PeCaruaruSpiderExecutive(BaseGazetteSpider):
    TERRITORY_ID = "2604106"
    allowed_domains = ["caruaru.pe.gov.br"]
    name = "pe_caruaru"
    start_urls = ["http://diario-oficial.caruaru.pe.gov.br/"]

    def parse(self, response):
        editions = json.loads(response.css("#diariosJSON::attr(data-items)").get())

        for edition in editions:
            yield Gazette(
                edition_number=re.search(r"(\d+)", edition["arquivo"]["url"]).group(1),
                date=date.fromisoformat(edition["arquivo"]["date"]),
                file_urls=[response.urljoin(edition["arquivo"]["url"])],
                is_extra_edition="Extra" in edition["resumo"],
                power="executive",
            )
