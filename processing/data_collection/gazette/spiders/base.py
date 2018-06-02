# -*- coding: utf-8 -*-
import dateparser
import scrapy


class BaseGazetteSpider(scrapy.Spider):
    def __init__(self, start_date=None, *args, **kwargs):
        super(BaseGazetteSpider, self).__init__(*args, **kwargs)

        if start_date is not None:
            parsed_data = dateparser.parse(start_date)
            if parsed_data is not None:
                self.start_date = parsed_data.date()
