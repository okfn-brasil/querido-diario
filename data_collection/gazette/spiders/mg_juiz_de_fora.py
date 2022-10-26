from datetime import date, timedelta
from urllib.parse import urljoin

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class MgJuizDeForaSpider(BaseGazetteSpider):
    TERRITORY_ID = "3136702"
    name = "mg_juiz_de_fora"
    allowed_domains = ["pjf.mg.gov.br"]
    start_urls = ["https://www.pjf.mg.gov.br/e_atos/e_atos.php"]
    base_files_url = "https://www.pjf.mg.gov.br/e_atos/"
    start_date = date(2010, 1, 5)
    end_date = date.today()
    # With scrapy's default headers, requests return error 500
    custom_settings = {
        "DEFAULT_REQUEST_HEADERS": {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0"
        },
    }
    # These acts were originally published with another id
    duplicated = [
        "https://www.pjf.mg.gov.br/e_atos/e_atos_vis.php?id=94851",
        "https://www.pjf.mg.gov.br/e_atos/e_atos_vis.php?id=57873",
        "https://www.pjf.mg.gov.br/e_atos/e_atos_vis.php?id=48631",
        "https://www.pjf.mg.gov.br/e_atos/e_atos_vis.php?id=8959",
    ]
    # These acts are linked to an annex originally published in another act
    have_duplicated_annex = [
        "https://www.pjf.mg.gov.br/e_atos/e_atos_vis.php?id=93137",
        "https://www.pjf.mg.gov.br/e_atos/e_atos_vis.php?id=60361",
        "https://www.pjf.mg.gov.br/e_atos/e_atos_vis.php?id=57384",
    ]

    def start_requests(self):
        curr_date = self.start_date
        while curr_date <= self.end_date:
            curr_date_str = curr_date.strftime("%d/%m/%Y")
            yield scrapy.FormRequest(
                self.start_urls[0],
                cb_kwargs={
                    "gazette_date": curr_date,
                },
                formdata={
                    "dataArea0": curr_date_str,
                    "dataArea1": curr_date_str,
                },
                method="POST",
            )
            curr_date += timedelta(days=1)

    def parse(self, response, gazette_date):
        acts_urls = [
            self.base_files_url + href
            for href in response.xpath(
                '//div[@class="atotextindex"]/p/a/@href'
            ).getall()
        ]
        for act_url in acts_urls:
            if act_url in self.duplicated:
                continue
            yield scrapy.Request(
                act_url,
                cb_kwargs={
                    "gazette_date": gazette_date,
                    "edition_number": "",
                    "file_urls": [act_url],
                },
                callback=self.parse_gazette,
            )

    def parse_gazette(self, response, gazette_date, file_urls, edition_number):
        annex = response.xpath('//td[@class="anexo"]/a/@href').get()
        if annex:
            if not (file_urls[0] in self.have_duplicated_annex):
                file_urls.append(urljoin(self.base_files_url, annex))
        yield Gazette(
            date=gazette_date,
            file_urls=file_urls,
            power="executive",
            is_extra_edition=False,
            edition_number=edition_number,
        )
