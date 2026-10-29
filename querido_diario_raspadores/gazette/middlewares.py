# -*- coding: utf-8 -*-
# Define here the models for your downloader middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
from scrapy.exceptions import CloseSpider
from scrapy_zyte_smartproxy import (
    ZyteSmartProxyMiddleware as BaseZyteSmartProxyMiddleware,
)

from gazette.utils.blocking import is_cloudflare_challenge


class ZyteSmartProxyMiddleware(BaseZyteSmartProxyMiddleware):
    """Expose scrapy-zyte-smartproxy through the current Scrapy middleware API."""

    def process_request(self, request):
        return super().process_request(request, self.spider)

    def process_response(self, request, response):
        return super().process_response(request, response, self.spider)

    def process_exception(self, request, exception):
        return super().process_exception(request, exception, self.spider)


class GazetteDownloaderMiddleware:
    # Uses the current Scrapy middleware API: methods don't receive the
    # spider as an argument (deprecated since Scrapy 2.14). The spider is
    # reached through the crawler saved in from_crawler().
    def __init__(self, crawler):
        self.crawler = crawler

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_response(self, request, response):
        # Called with the response returned from the downloader.
        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        if is_cloudflare_challenge(response):
            self.crawler.stats.inc_value("cloudflare_challenge/blocked_count")
            self.crawler.spider.logger.error(
                "Blocked by a Cloudflare Turnstile challenge at %s. Aborting "
                "the spider instead of treating the challenge page as valid "
                "content.",
                request.url,
            )
            # Raised here, this is caught the same way an exception raised
            # from a spider callback would be: it stops the spider with a
            # finish_reason that isn't "finished", which our Spidermon
            # monitors (FinishReasonMonitor/ErrorCountMonitor) already treat
            # as a failure. For requests started by the files pipeline
            # (downloading the gazette PDF), this is instead caught by
            # Scrapy's MediaPipeline as a failed download, so the fake file
            # is dropped rather than saved as if it were the real gazette.
            raise CloseSpider(reason="blocked_by_cloudflare_turnstile")
        return response
