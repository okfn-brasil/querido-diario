import dateparser
from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class BaseAtendeT2Spider(BaseGazetteSpider):
    """
    Base spider for Gazzetes that are available from cities listed on https://{city_subdomain}.atende.net
    This base class deals with layout 'Type 2' gazette pages, usually requested
    from 'https://{city_subdomain}.atende.net/diariooficial'.
    """

    # Must be defined into child classes
    city_subdomain = ""

    power = "executive_legislative"

    start_page = 1
    end_page = 0
    extra_edition_options = ("suplementar", "retificação", "extraordinária", "extra")
    allowed_domains = ["atende.net"]

    def start_requests(self):
        yield Request(self.get_url(self.start_page))

    def parse(self, response, page=start_page):
        lines = response.css("div.nova_listagem div.linha")
        for line in lines:
            date_raw = line.css("div.data::text").get()
            date_time = dateparser.parse(date_raw, languages=["pt"])
            if date_time is None:
                self.logger.debug(f"Unable to parse date from text {date_raw}!")
                continue
            date = date_time.date()

            if date > self.end_date:
                continue
            if date < self.start_date:
                return

            edition_type = line.css("div.tipo::text").get()
            is_extra = (
                edition_type.lower() in self.extra_edition_options
                if edition_type
                else False
            )
            edition_number = line.css("div.titulo::text").get()
            # edition_number = lines.css("div.titulo::text").re_first(r"[^\s][\d.]+")
            download_urls = line.css("button::attr(data-link)")
            if len(download_urls) < 1:
                self.logger.debug("Unable to find an url for download!")
                continue
            download_url = download_urls[-1].get()

            yield Gazette(
                date=date,
                edition_number=edition_number,
                file_urls=[download_url],
                is_extra_edition=is_extra,
                power=self.power,
            )

        if self.end_page < 1:
            pages = response.css("div#paginacao li.dst button::attr(value)").getall()
            if len(pages) > 1:
                self.end_page = int(pages[-1])
            else:
                self.logger.debug("Unable to find the last page!")

        page += 1
        if page <= self.end_page:
            yield response.follow(self.get_url(page), cb_kwargs={"page": page})

    def get_url(self, page):
        return f"https://{self.city_subdomain}.atende.net/diariooficial/edicao/pagina/atende.php?rot=54015&aca=101&ajax=t&processo=loadPluginDiarioOficial&parametro=%7B%22codigoPlugin%22%3A1,%22filtroPlugin%22%3A%7B%22pagina%22%3A%22{page}%22%7D%7D"
