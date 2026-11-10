import json
import math
from datetime import datetime

from scrapy import Request
from scrapy.exceptions import NotConfigured

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class BaseEatosSpider(BaseGazetteSpider):
    """
    Base Spider for municipalities that publish their gazettes using eatos
    (https://publicacoesmunicipais.com.br/eatos/<url_path>)

    The API lists the editions from the newest to the oldest and the PDF of
    each edition can be downloaded directly with the municipality path and
    the edition number.

    Attributes
    ----------
    url_path : str
        It must be defined in child classes.
        The municipality identifier used by eatos in its URLs
        e.g:
            - maripa, for https://publicacoesmunicipais.com.br/eatos/maripa
            - smi, for https://publicacoesmunicipais.com.br/eatos/smi
    """

    allowed_domains = ["api.publicacoesmunicipais.com.br"]
    api_url = "https://api.publicacoesmunicipais.com.br/api"
    page_size = 100
    power = "executive"

    def __init__(self, *args, **kwargs):
        if not hasattr(self, "url_path"):
            raise NotConfigured("Please set a value for `url_path`")

        super(BaseEatosSpider, self).__init__(*args, **kwargs)

    async def start(self):
        yield self._acts_request(page=1)

    def _acts_request(self, page):
        return Request(
            f"{self.api_url}/v1/acts?page={page}&pageSize={self.page_size}"
            f"&urlPath={self.url_path}",
            callback=self.parse,
            cb_kwargs={"page": page},
        )

    def parse(self, response, page):
        payload = json.loads(response.text)
        acts = payload.get("acts") or []

        gazette_dates = []
        for act in acts:
            gazette_date = datetime.fromisoformat(act["date"]).date()
            gazette_dates.append(gazette_date)

            if not self.start_date <= gazette_date <= self.end_date:
                continue

            edition_number = act["edition"]
            yield Gazette(
                date=gazette_date,
                edition_number=edition_number,
                is_extra_edition=False,
                file_urls=[f"{self.api_url}/v2/acts/{self.url_path}/{edition_number}"],
                power=self.power,
            )

        total_pages = math.ceil(payload.get("total", 0) / self.page_size)
        # The editions come from the newest to the oldest, so the next pages
        # only have older editions once this page passed the start date.
        if (
            page < total_pages
            and gazette_dates
            and min(gazette_dates) >= self.start_date
        ):
            yield self._acts_request(page=page + 1)
