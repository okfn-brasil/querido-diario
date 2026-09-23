import asyncio
import gzip
from unittest.mock import MagicMock

import pytest
from scrapy import Spider
from scrapy.core.downloader.middleware import DownloaderMiddlewareManager
from scrapy.exceptions import CloseSpider
from scrapy.http import HtmlResponse, Request, TextResponse
from scrapy.settings.default_settings import DOWNLOADER_MIDDLEWARES_BASE
from scrapy.utils.reactor import install_reactor
from scrapy.utils.test import get_crawler

from gazette import settings
from gazette.middlewares import GazetteDownloaderMiddleware
from gazette.utils.blocking import is_cloudflare_challenge

install_reactor("twisted.internet.asyncioreactor.AsyncioSelectorReactor")


def make_response(body: bytes, status: int = 200, url: str = "https://example.org"):
    return TextResponse(url=url, body=body, status=status)


class TestIsCloudflareChallenge:
    def test_real_gazette_page_is_not_a_challenge(self):
        response = make_response(b"<html><body>Diario Oficial</body></html>")
        assert is_cloudflare_challenge(response) is False

    def test_real_pdf_is_not_a_challenge(self):
        response = make_response(b"%PDF-1.4 some binary pdf content")
        assert is_cloudflare_challenge(response) is False

    @pytest.mark.parametrize(
        "marker",
        [
            b"challenges.cloudflare.com",
            b"cf-turnstile",
            b"cf_chl_opt",
            b"Just a moment...",
            b"Attention Required! | Cloudflare",
        ],
    )
    def test_detects_known_turnstile_markers(self, marker):
        response = make_response(
            b"<html><head><title>%s</title></html>" % marker, status=403
        )
        assert is_cloudflare_challenge(response) is True

    def test_marker_outside_inspection_window_is_not_detected(self):
        padding = b"x" * 8192
        response = make_response(padding + b"cf-turnstile")
        assert is_cloudflare_challenge(response) is False


class TestGazetteDownloaderMiddleware:
    def setup_method(self):
        self.middleware = GazetteDownloaderMiddleware()
        self.spider = MagicMock()
        self.spider.crawler.stats = MagicMock()
        self.request = Request("https://example.org")

    def test_returns_response_when_not_blocked(self):
        response = make_response(b"<html>real content</html>")
        result = self.middleware.process_response(self.request, response, self.spider)
        assert result is response
        self.spider.crawler.stats.inc_value.assert_not_called()

    def test_raises_close_spider_when_blocked(self):
        response = make_response(b"cf-turnstile challenge page", status=403)
        with pytest.raises(CloseSpider) as exc_info:
            self.middleware.process_response(self.request, response, self.spider)
        assert exc_info.value.reason == "blocked_by_cloudflare_turnstile"
        self.spider.crawler.stats.inc_value.assert_called_once_with(
            "cloudflare_challenge/blocked_count"
        )


class TestMiddlewareOrderInProjectSettings:
    """Challenge pages are usually served gzip-encoded, so the detection
    only works if it runs after Scrapy's HttpCompressionMiddleware has
    decoded the body."""

    def download_through_project_middlewares(self, response_kwargs):
        # Only the two components that matter here, each at the priority it
        # really has: Scrapy's default for decompression, ours from settings.
        compression = (
            "scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware"
        )
        gazette = "gazette.middlewares.GazetteDownloaderMiddleware"
        crawler = get_crawler(
            Spider,
            settings_dict={
                "DOWNLOADER_MIDDLEWARES_BASE": {
                    compression: DOWNLOADER_MIDDLEWARES_BASE[compression]
                },
                "DOWNLOADER_MIDDLEWARES": {
                    gazette: settings.DOWNLOADER_MIDDLEWARES[gazette]
                },
            },
        )
        crawler.spider = crawler._create_spider("test")
        manager = DownloaderMiddlewareManager.from_crawler(crawler)
        manager._set_compat_spider(crawler.spider)

        async def download(request):
            return HtmlResponse(request=request, url=request.url, **response_kwargs)

        request = Request("https://example.org/arquivos_download.php?id=1")
        return asyncio.run(manager.download_async(download, request))

    def test_detects_challenge_in_gzip_encoded_response(self):
        challenge_page = (
            b"<html><head><title>Prefeitura</title></head><body>"
            b'<div class="cf-turnstile"></div>'
            b'<script src="https://challenges.cloudflare.com/turnstile/v0/api.js">'
            b"</script></body></html>"
        )
        with pytest.raises(CloseSpider):
            self.download_through_project_middlewares(
                {
                    "body": gzip.compress(challenge_page),
                    "headers": {"Content-Encoding": "gzip"},
                }
            )

    def test_gzip_encoded_real_content_passes_through(self):
        response = self.download_through_project_middlewares(
            {
                "body": gzip.compress(b"%PDF-1.4 real gazette"),
                "headers": {"Content-Encoding": "gzip"},
            }
        )
        assert response.body == b"%PDF-1.4 real gazette"
