import datetime as dt

from scrapy import FormRequest

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class MgUberabaSpider(BaseGazetteSpider):
    TERRITORY_ID = "3170107"
    name = "mg_uberaba_2003"
    allowed_domains = ["uberaba.mg.gov.br"]

    start_date = dt.date(2003, 4, 25)
    end_date = dt.date(2021, 9, 1)

    def start_requests(self):
        for year in range(self.start_date.year, self.end_date.year + 1):
            yield FormRequest(
                url="http://www.uberaba.mg.gov.br/portal/listImagesHtml",
                method="POST",
                formdata={
                    "desc": "1",
                    "type": "1",
                    "folder": f"portavoz/arquivos/{year}",
                    "limit": "5000",
                    "page": "1",
                    "types": "gif,jpg,png,bmp,tif,dxf,swf,dcr,mov,qt,ram,rm,avi,mpg,mpeg,asf,flv,pdf,doc,docx,xls,xlsx,zip,rar,txt,cdr,ai,eps,ppt,pptx,pot,psd,wmv",
                    "listAll": "1",
                },
            )

    def parse(self, response):
        gazettes = response.css(".claGaleriaBoxFileTable")
        for gazette in gazettes:
            raw_date = gazette.css("::text").re_first(r"(\d{2}-\d{2}-\d{4})")
            try:
                gazette_date = dt.datetime.strptime(raw_date, "%d-%m-%Y").date()
            except Exception:
                self.logger.error(
                    f"Gazette date can't be parsed from gazette named \"{gazette.css('::text').get()}\""
                )
                continue

            if gazette_date > self.end_date:
                continue
            elif gazette_date < self.start_date:
                return

            gazette_url = response.urljoin(
                gazette.css("img::attr(onclick)").re_first(r"download\(\'(.*)\'\)")
            )
            edition_number = gazette.css("::text").re_first(r"^\s*?(\d{4})")

            yield Gazette(
                date=gazette_date,
                file_urls=[
                    gazette_url,
                ],
                is_extra_edition=False,
                edition_number=edition_number,
                power="executive_legislative",
            )
