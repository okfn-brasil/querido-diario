import datetime as dt
import re

from scrapy import FormRequest

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider
from gazette.spiders.base.dosp import DospGazetteSpider


class MgUberabaSpider(DospGazetteSpider):
    TERRITORY_ID = "3170107"
    name = "mg_uberaba"

    code = 2364
    start_date = dt.date(2021, 9, 1)


class MgUberabaAcervo2003A2021Spider(BaseGazetteSpider):
    TERRITORY_ID = "3170107"
    name = "mg_uberaba_acervo_2003_a_2021"
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
        filenames = [
            filename.strip()
            for filename in response.css("div.claGaleriaBoxFileTable::text").getall()
        ]
        for filename in filenames:
            raw_date = re.search(r"\d{2}-\d{2}-\d{4}", filename)
            if raw_date is None:
                continue

            date = dt.datetime.strptime(raw_date.group(), "%d-%m-%Y").date()
            if self.start_date > date > self.end_date:
                continue

            base_download_url = (
                "http://www.uberaba.mg.gov.br:8080/portal/acervo/portavoz/arquivos"
            )
            url = f"{base_download_url}/{date.year}/{filename}"
            edition_number = re.match(r"\d+", filename).group().lstrip("0")

            yield Gazette(
                date=date,
                file_urls=[url],
                edition_number=edition_number,
                power="executive_legislative",
            )
