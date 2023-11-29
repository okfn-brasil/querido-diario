import datetime as dt
import locale

import dateparser
from dateutil.relativedelta import relativedelta
from dateutil.rrule import MONTHLY, rrule
from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class BaseAtendeT1Spider(BaseGazetteSpider):
    """
    Base spider for Gazzetes that are available from cities listed on https://{city_subdomain}.atende.net
    This base class deals with layout 'Type 1' gazette pages, usually requested
    from 'https://{city_subdomain}.atende.net/cidadao/pagina/diario-oficial'.
    """

    # Must be defined into child classes
    city_subdomain = ""
    perm_url = ""

    start_edition = 0
    power = "executive_legislative"
    extra_edition_options = ("extra", "anexo", "segunda", "2ª", "especial", "decreto")
    allowed_domains = ["atende.net"]

    def start_requests(self):
        locale.setlocale(locale.LC_ALL, "pt_BR.utf8")
        yield Request(self.get_url(self.perm_url))

    def parse(self, response):
        # cachoeirinha files aren't available in the first page. They are in month pages.
        month_pages = response.css("a.itemPaginasRelacionadas::attr(href)")
        if len(month_pages) > 0:
            # There is no link for 05/2016 in the first page.
            # for month_page in month_pages:
            #     yield Request(self.get_url(month_page.split("/")[-1]), self.parse)
            monthly_rec = rrule(
                MONTHLY,
                dtstart=self.start_date + relativedelta(day=1),
                until=self.end_date,
            )[::-1]
            month_urls = [
                self.get_url(f"diario-oficial-{rec.strftime('%B-%Y')}")
                for rec in monthly_rec
            ]
            for month_url in month_urls:
                yield Request(month_url, self.parse)
        else:
            click_links = response.css("div.arquivos a::attr(onclick)")
            title_list = response.css("div.arquivos li::attr(data-original-title)")
            if len(click_links) != len(title_list):
                self.logger.warning(
                    f"Size of titles ({len(title_list)}) not equal to size of links ({len(click_links)})!"
                )
            for link, title in zip(click_links, title_list):
                edition_number = title.re_first(r"[^\s/-][\d]+")
                date_raw = title.re(
                    r"(\d{1,4})?[_ -]*([\dº]{2})[/._-](\d{2})[/._-](\d{2,4})"
                )
                date_time = dateparser.parse(
                    ("/".join(date_raw[1:])).replace("º", ""), languages=["pt"]
                )
                if date_time is None:
                    # self.logger.debug(f"Unable to parse date from {date_raw[1:]}!")
                    if not edition_number:
                        self.logger.debug(
                            f"Unable to parse edition number from '{title.get()}'!"
                        )
                        continue
                    # date will be extracted from gazette in data processing stage.
                    gazette_date = dt.date.max
                else:
                    gazette_date = date_time.date()
                    if not (self.start_date <= gazette_date <= self.end_date):
                        continue
                if edition_number and int(edition_number) < self.start_edition:
                    continue
                edition = title.get().strip()
                is_extra = self.is_extra_edition(edition.lower())
                file_id = link.re_first(r"arquivo\('(\w+)")
                download_url = f"{self.get_base_url()}?rot=1&aca=571&ajax=t&processo=downloadFile&file={file_id}&sistema=WPO&classe=UploadMidia"
                yield Gazette(
                    date=gazette_date,
                    edition_number=edition,
                    file_urls=[download_url],
                    is_extra_edition=is_extra,
                    power=self.power,
                )

    def is_extra_edition(self, edition_text):
        for option in self.extra_edition_options:
            if option in edition_text:
                return True
        return False

    def get_base_url(self):
        return f"https://{self.city_subdomain}.atende.net/cidadao/pagina/atende.php"

    def get_url(self, p_url):
        return f"{self.get_base_url()}?rot=49094&aca=101&ajax=t&processo=loadPluginPortal&parametro=%7B%22codigoPlugin%22%3A65,%22parametroPlugin%22%3A%7B%22loadDetalhes%22%3Atrue%7D,%22filtroPlugin%22%3A%7B%22paginaUrlPermanente%22%3A%22{p_url}%22%7D%7D"


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
            gazette = Gazette(
                date=date,
                edition_number=edition_number,
                is_extra_edition=is_extra,
                power=self.power,
            )
            download_urls = line.css("button::attr(data-link)")
            if len(download_urls) > 0:
                gazette["file_urls"] = [download_urls[-1].get()]
                yield gazette
            else:
                # self.logger.debug("Unable to find an url for download! Trying edition details.")
                edition_id = line.css("span.bt_detalhes::attr(data-id)").get()
                edition_url = f"{self.get_base_url()}&parametro=%7B%22codigoPlugin%22%3A2,%22filtroPlugin%22%3A%7B%22codigoEdicao%22%3A%22{edition_id}%22%7D%7D"
                yield Request(
                    edition_url, self.parse_edition, cb_kwargs={"gazette": gazette}
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

    def parse_edition(self, response, gazette):
        download_url = response.css(
            "button.visualizacao_versao_completa::attr(data-link)"
        ).get()
        gazette["file_urls"] = [download_url]
        yield gazette

    def get_base_url(self):
        return f"https://{self.city_subdomain}.atende.net/diariooficial/edicao/pagina/atende.php?rot=54015&aca=101&ajax=t&processo=loadPluginDiarioOficial"

    def get_url(self, page):
        return f"{self.get_base_url()}&parametro=%7B%22codigoPlugin%22%3A1,%22filtroPlugin%22%3A%7B%22pagina%22%3A%22{page}%22%7D%7D"
