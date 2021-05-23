import datetime

from dateparser import parse

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class PrCampoMouraoSpider(BaseGazetteSpider):
    TERRITORY_ID = "4104303"
    name = "pr_campo_mourao"
    start_date = datetime.date(2012, 3, 2)
    start_urls = ["https://campomourao.atende.net/?pg=diariooficial&pagina=1"]

    def parse(self, response, page=1):

        gazettes = response.xpath("//div[@class='nova_listagem ']/div[@class='linha']")
        follow_next_page = False if not gazettes else True

        for gazette in gazettes:
            date = gazette.xpath(".//div[@class='data']/text()").get()
            date = parse(date, languages=["pt"]).date()

            if date < self.start_date:
                follow_next_page = False
                break

            edition_type = gazette.xpath(".//div[@class='tipo']/text()").get()
            edition_number = gazette.xpath(".//div[@class='titulo']/text()").get()
            edition_number = edition_number.split(" ")[1]

            code = gazette.xpath("//button[@data-acao='download']/@data-codigo").get()
            id = gazette.xpath("//button[@data-acao='download']/@data-id").get()

            is_extra = True if edition_type == "Extraordinária" else False

            url = f"https://campomourao.atende.net/atende.php?rot=54002&aca=737&processo=download&codigo={code}&hash={id}"

            yield Gazette(
                date=date,
                edition_number=edition_number,
                file_urls=[url],
                is_extra_edition=is_extra,
                power="executive_legislative",
            )

        if follow_next_page:
            next_page = page + 1
            yield response.follow(
                f"https://campomourao.atende.net/?pg=diariooficial&pagina={next_page}",
                cb_kwargs={"page": next_page},
            )
