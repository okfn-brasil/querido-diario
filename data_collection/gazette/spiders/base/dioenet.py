import datetime as dt
import re

from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class BaseDioenetSpider(BaseGazetteSpider):
    def start_requests(self):
        start_date = self.start_date.strftime("%d/%m/%Y")
        end_date = self.end_date.strftime("%d/%m/%Y")

        yield Request(f"{self.BASE_URL}?secao=&d={start_date}+a+{end_date}")

    def parse(self, response):
        gazettes = response.xpath("//ul[@class='lista-diarios']/li")

        for gazette in gazettes:
            date = gazette.css("h3::text").get()
            date = re.search(r"\d{2}/\d{2}/\d{4}", date).group()
            gazette_date = dt.datetime.strptime(date, "%d/%m/%Y").date()

            if gazette_date < self.start_date:
                break

            edition_number = gazette.css("span::text").get().split()[-1]

            pdf_url = gazette.css("a::attr(href)").get()

            if pdf_url.endswith(".pdf"):
                gazette_url = pdf_url
                yield Gazette(
                    date=gazette_date,
                    edition_number=edition_number,
                    file_urls=[gazette_url],
                    is_extra_edition=False,
                    power="executive",
                )

            else:
                item = Gazette(
                    date=gazette_date,
                    edition_number=edition_number,
                    is_extra_edition=False,
                    power="executive",
                )

                yield Request(
                    response.urljoin(pdf_url),
                    callback=self.get_url,
                    cb_kwargs={"item": item},
                )

        next_page = gazettes.xpath(
            "//a[contains(text(), 'Próximo')]/@data-ci-pagination-page"
        ).get()
        if next_page is not None:
            yield Request(
                response.request.url.split("&pagina=")[0] + f"&pagina={next_page}"
            )

    def get_url(self, response, item):
        if response.xpath("//div[@id='content']/iframe/@src").get() is not None:
            gazette_url = (
                response.xpath("//div[@id='content']/iframe/@src")
                .get()
                .split("file=")[-1]
            )
            yield Gazette(
                file_urls=[gazette_url],
                **item,
            )
        else:
            pass
