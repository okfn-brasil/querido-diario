import json
from dateparser import parse
import datetime as dt

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RnFederacaoMunicipiosSpider(BaseGazetteSpider):

    TERRITORY_ID = "2400000"

    name = "rn_federacao_municipios"

    allowed_domains = ["diariomunicipal.com.br"]
    start_urls = ["http://www.diariomunicipal.com.br/femurn"]

    def parse(self, response):
        token = response.xpath('//input[@id="calendar__token"]/@value').get()
        date = dt.date.today()
        while date >= dt.date(2009, 10, 2):
            formdata = {
                "calendar[_token]": token,
                "calendar[day]": str(date.day),
                "calendar[month]": str(date.month),
                "calendar[year]": str(date.year),
            }
            yield scrapy.FormRequest(
                response.url + "materia/calendario",
                formdata=formdata,
                callback=self.parse_gazette,
            )
            yield scrapy.FormRequest(
                response.url + "materia/calendario/extra",
                formdata=formdata,
                callback=self.parse_gazette,
            )
            date -= dt.timedelta(days=1)

    def parse_gazette(self, response):
        data = json.loads(response.text or "null")
        if data and not data.get("error"):
            url = data["url_arquivos"]
            for edicao in data["edicao"]:
                url = url + edicao["link_diario"] + ".pdf"
                date = parse(edicao["data_circulacao"]).date()
                yield Gazette(
                    date=date,
                    file_urls=[url],
                    is_extra_edition=edicao["is_extraordinario"],
                    territory_id=self.TERRITORY_ID,
                    power="executive",
                    scraped_at=dt.datetime.utcnow(),
                )
