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

    def __init__(self, start_date=None, end_date=None, *args, **kwargs):
        super(BaseGazetteSpider, self).__init__(*args, **kwargs)

        if not hasattr(self, "TERRITORY_ID"):
            raise NotConfigured("Please set a value for `TERRITORY_ID`")

        if start_date is not None:
            try:
                self.start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            except ValueError:
                self.logger.exception(
                    f"Unable to parse {start_date}. Use %Y-%m-d date format."
                )
                raise

        self.end_date = datetime.today().date()
        if end_date is not None:
            try:
                self.end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
            except ValueError:
                self.logger.exception(
                    f"Unable to parse {end_date}. Use %Y-%m-d date format."
                )
                raise

        self.logger.info(f"Collecting data from {self.start_date} to {self.end_date}.")
