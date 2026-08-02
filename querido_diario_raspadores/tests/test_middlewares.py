import warnings

from scrapy import Request, Spider
from scrapy.core.downloader.middleware import DownloaderMiddlewareManager
from scrapy.exceptions import ScrapyDeprecationWarning
from scrapy.utils.reactor import install_reactor
from scrapy.utils.test import get_crawler

from gazette.middlewares import ZyteSmartProxyMiddleware

install_reactor("twisted.internet.asyncioreactor.AsyncioSelectorReactor")


def build_middleware(enabled):
    crawler = get_crawler(
        Spider,
        settings_dict={
            "DOWNLOADER_MIDDLEWARES": {
                "gazette.middlewares.ZyteSmartProxyMiddleware": 610,
            },
            "ZYTE_SMARTPROXY_APIKEY": "test-key",
            "ZYTE_SMARTPROXY_ENABLED": enabled,
        },
    )
    middleware = ZyteSmartProxyMiddleware.from_crawler(crawler)
    middleware.open_spider(Spider(name="test"))
    return crawler, middleware


def test_zyte_middleware_uses_current_scrapy_signatures():
    crawler = get_crawler(
        Spider,
        settings_dict={
            "DOWNLOADER_MIDDLEWARES": {
                "gazette.middlewares.ZyteSmartProxyMiddleware": 610,
            }
        },
    )

    with warnings.catch_warnings(record=True) as caught_warnings:
        DownloaderMiddlewareManager.from_crawler(crawler)

    zyte_deprecations = [
        warning
        for warning in caught_warnings
        if issubclass(warning.category, ScrapyDeprecationWarning)
        and "ZyteSmartProxyMiddleware" in str(warning.message)
    ]
    assert zyte_deprecations == []


def test_zyte_middleware_does_not_proxy_when_disabled():
    _, middleware = build_middleware(enabled=False)
    request = Request("https://example.com")

    middleware.process_request(request)

    assert "proxy" not in request.meta


def test_zyte_middleware_preserves_proxy_behavior_when_enabled():
    crawler, middleware = build_middleware(enabled=True)
    request = Request("https://example.com")

    middleware.process_request(request)

    assert request.meta["proxy"].startswith("http://test-key:")
    assert crawler.stats.get_value("zyte_smartproxy/request") == 1
