from datetime import datetime

import scrapy
from scrapy.exceptions import NotConfigured


class BaseGazetteSpider(scrapy.Spider):
    # Some websites block access from servers outside
    # Brazil. We are running our spiders in Scrapy Cloud
    # (https://www.zyte.com/scrapy-cloud/) and its servers
    # are not in Brazil. To allow us to get that data, we
    # can enable Zyte Smart Proxy (a paid service). Only
    # enable this in your spider after ensuring that we are
    # being blocked based on our location.
    zyte_smartproxy_enabled = False

    def __init__(self, start=None, end=None, *args, **kwargs):
        super(BaseGazetteSpider, self).__init__(*args, **kwargs)

        if not hasattr(self, "TERRITORY_ID"):
            raise NotConfigured("Please set a value for `TERRITORY_ID`")

        if not hasattr(self, "allowed_domains"):
            raise NotConfigured("Please set a value for `allowed_domains`")

        if not hasattr(self, "start_date"):
            raise NotConfigured("Please set a value for `start_date`")

        if start:
            try:
                self.start_date = datetime.strptime(start, "%Y-%m-%d").date()
            except ValueError:
                self.logger.exception(
                    f"Unable to parse {start}. Use %Y-%m-d date format."
                )
                raise

        if end:
            try:
                self.end_date = datetime.strptime(end, "%Y-%m-%d").date()
            except ValueError:
                self.logger.exception(
                    f"Unable to parse {end}. Use %Y-%m-d date format."
                )
                raise
        else:
            self.end_date = datetime.today().date()

        self.logger.info(f"Collecting data from {self.start_date} to {self.end_date}.")
