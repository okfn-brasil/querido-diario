from unittest.mock import MagicMock

import pytest
from scrapy.exceptions import CloseSpider
from scrapy.http import Request, TextResponse

from gazette.middlewares import GazetteDownloaderMiddleware
from gazette.utils.blocking import is_cloudflare_challenge


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
