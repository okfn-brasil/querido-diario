from datetime import datetime

import scrapy

from gazette.exceptions import WrongTimespan
from gazette.utils import territories_metadata


class BaseGazetteSpider(scrapy.Spider):
    # Some websites block access from servers outside
    # Brazil. We are running our spiders in Scrapy Cloud
    # (https://www.zyte.com/scrapy-cloud/) and its servers
    # are not in Brazil. To allow us to get that data, we
    # can enable Zyte Smart Proxy (a paid service). Only
    # enable this in your spider after ensuring that we are
    # being blocked based on our location.
    zyte_smartproxy_enabled = False

    def __init__(self, start_date=None, end_date=None, *args, **kwargs):
        super(BaseGazetteSpider, self).__init__(*args, **kwargs)

        if not hasattr(self, "TERRITORY_ID"):
            raise AttributeError("Please set a value for `TERRITORY_ID`")

        if not self._is_valid_spidername(self.name):
            raise ValueError(
                "Spider name should start with territories.csv spider_prefix column"
            )

        _start_date = self._parse_date_arguments(start_date, self.start_date)
        self.start_date = max([_start_date, self.start_date])

        default_end_date = datetime.today().date()
        _end_date = self._parse_date_arguments(end_date, default_end_date)
        self.end_date = min([_end_date, getattr(self, "end_date", default_end_date)])

        if self.start_date > self.end_date:
            raise WrongTimespan("Start date can't be after end date.")

        self.logger.info(
            f"Collecting gazettes from {self.start_date} until {self.end_date}"
        )

    def _is_valid_spidername(self, name):
        for territory in territories_metadata():
            if name.startswith(territory["spider_prefix"]):
                return True
        else:
            return False

    def _parse_date_arguments(self, date, default):
        if date is None:
            return default

        try:
            parsed = datetime.strptime(date, "%Y-%m-%d").date()
            return parsed
        except ValueError:
            self.logger.exception(f"Unable to parse {date}. Use %Y-%m-d date format.")
            raise
