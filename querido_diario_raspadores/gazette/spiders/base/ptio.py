import scrapy
from scrapy.exceptions import NotConfigured

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider
from gazette.utils.extraction import get_date_from_text


class BasePtioSpider(BaseGazetteSpider):
    allowed_domains = ["portaldatransparencia.com.br"]

    def __init__(self, *args, **kwargs):
        if not hasattr(self, "BASE_URL"):
            raise NotConfigured("Please set a value for `BASE_URL`")

        super(BasePtioSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        yield scrapy.Request(self.BASE_URL)

    def parse(self, response):
        for gazette_div in response.xpath("//div[@class='edicoes']"):
            raw_gazete_date = gazette_div.xpath(
                ".//div[@class='data-caderno hidden-phone']/text()"
            ).get()
            gazette_date = get_date_from_text(raw_gazete_date)

            if gazette_date > self.end_date:
                continue
            if gazette_date < self.start_date:
                return

            gazette_edition = gazette_div.xpath(
                ".//span[@class='edicao']/strong/text()"
            ).get()
            gazette_edition_number = gazette_edition.split()[1].replace(".", "")

            sub_dir = gazette_div.xpath(".//button[1]/@href").get()
            gazette_url = response.urljoin(sub_dir[sub_dir.index("?") :])

            yield Gazette(
                date=gazette_date,
                edition_number=gazette_edition_number,
                is_extra_edition=False,
                file_urls=[gazette_url],
                power="executive",
            )

        next_page = response.xpath(
            "//ul[@class='paginacao']//a[@class='proximo']/@href"
        )
        if next_page:
            yield scrapy.Request(response.urljoin(next_page.get()))
