import datetime

from scrapy import FormRequest, Selector

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class ToLavandeira2020(BaseGazetteSpider):
    TERRITORY_ID = "1712157"
    name = "to_lavandeira_2020"
    allowed_domains = ["futurosistemasadm.hospedagemdesites.ws"]
    start_date = datetime.date(2017, 2, 27)
    end_date = datetime.date(2020, 5, 20)
    BASE_URL = "http://futurosistemasadm.hospedagemdesites.ws/prefeituradelavandeira/diarioeletronico/projeto_cadastro"

    def start_requests(self):
        yield FormRequest(
            f"{self.BASE_URL}/pesquisatodososdiarios.php", formdata={"enviado": "S"}
        )

    def parse(self, response):
        rows = response.xpath("//tr[@bgcolor='#FFF']").getall()

        for row in rows:
            selector = Selector(text=row)

            cols_1_and_2 = selector.xpath("//font/text()").getall()

            date = datetime.datetime.strptime(cols_1_and_2[0], "%d/%m/%Y").date()
            edition = cols_1_and_2[1]

            url = f"{self.BASE_URL}/{selector.xpath('//a/@href').get()}"

            yield Gazette(
                date=date,
                file_urls=[url],
                is_extra_edition=False,
                edition_number=edition,
                power="executive",
            )
