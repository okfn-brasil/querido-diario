import logging
import random
import re
from datetime import date, datetime

import scrapy
from dateutil.rrule import DAILY, rrule

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider

user_agent_list = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
    "Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363",
]


class SpSaoPauloSpider(BaseGazetteSpider):
    TERRITORY_ID = "3550308"
    BASE_URL = "https://diariooficial.prefeitura.sp.gov.br"
    allowed_domains = ["diariooficial.prefeitura.sp.gov.br"]
    name = "sp_sao_paulo"
    start_date = date(2017, 6, 1)
    end_date = date.today()
    # RETRY_HTTP_CODES = [500, 503, 504, 400, 408, 307, 403]
    custom_settings = {
        "CONCURRENT_REQUESTS": 1,
        "DOWNLOAD_DELAY": 2,
        "RANDOMIZE_DOWNLOAD_DELAY": True,
        "DEFAULT_REQUEST_HEADERS": {
            "Referer": f"{BASE_URL}",
            #'User-Agent': user_agent_list[random.randint(0, len(user_agent_list)-1)],
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "pt-BR,pt;q=0.9",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "sec-ch-ua": '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
        },
    }

    def start_requests(self):
        url = (
            f"{self.BASE_URL}/md_epubli_controlador.php?acao=edicao_consultar&formato=A"
        )
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        dates = list(rrule(freq=DAILY, dtstart=self.start_date, until=self.end_date))
        random.shuffle(dates)
        for day in dates:
            formdata = {
                "hdnDtaEdicao": day.strftime("%d/%m/%Y"),
                "hdnTipoEdicao": "C",
                "hdnBolEdicaoGerada": "False",
                "hdnIdEdicao": "",
                "hdnInicio": "0",
                "hdnFormato": "A",
            }
            yield scrapy.FormRequest(
                url=f"{self.BASE_URL}/md_epubli_controlador.php?acao=edicao_consultar",
                method="POST",
                formdata=formdata,
                callback=self.parse_main,
                cb_kwargs=dict(date=day),
            )

    def parse_main(self, response, date):
        gazette_date = date.date()
        edicaotitulo = response.css(".edicaotitulo::text").get()
        logging.debug(f"gazette_date={gazette_date}, edicaotitulo={edicaotitulo}")

        eh_captcha = (
            "Este desafio é para testar se você é um visitante humano."
            in response.css("body").get()
        )
        if eh_captcha:
            logging.warn(f"Captcha Enabled! Skipping date={gazette_date}")
        if not eh_captcha:
            if edicaotitulo is not None:
                (
                    gazette_edition_number,
                    gazette_year,
                ) = self.extract_year_and_edition_number(edicaotitulo)
            url_download_pdf = response.css(
                "#skipto-content > div.container > div > div > div > div:nth-child(2) > div.container-fluid > div > div:nth-child(2) > a:nth-child(2)::attr(href)"
            ).get()
            if url_download_pdf is not None:
                urls = [url_download_pdf]
                yield Gazette(
                    date=gazette_date,
                    file_urls=urls,
                    edition_number=gazette_edition_number,
                    is_extra_edition=False,
                    territory_id=self.TERRITORY_ID,
                    power="executive",
                    scraped_at=datetime.utcnow(),
                )

    def extract_year_and_edition_number(self, text):
        RE = re.compile(r"\b(\d+)\b.*?\b(\d+)\b")
        match = RE.search(text.strip())
        if match:
            m1 = match.group(1)
            m2 = match.group(2)
            return (m1, m2)
        else:
            return ("", "")
