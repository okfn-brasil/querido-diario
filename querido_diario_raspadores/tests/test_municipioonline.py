import asyncio
from datetime import date

from scrapy.http import HtmlResponse, Request
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.python.failure import Failure

from gazette.spiders.base.municipioonline import BaseMunicipioOnlineSpider

FORM_HTML = b"""
<html><body>
<form method="post" action="./diariooficial">
  <input type="hidden" name="__VIEWSTATE" value="state" />
  <input type="text" name="ctl00$body$txtDtPeriodo" value="" />
</form>
</body></html>
"""
URL = "https://www.municipioonline.com.br/se/prefeitura/teste/cidadao/diariooficial"


class MunicipioOnlineSpiderForTest(BaseMunicipioOnlineSpider):
    TERRITORY_ID = "0000000"
    name = "municipioonline_test"
    url_uf = "se"
    url_city = "teste"
    start_date = date(2024, 3, 10)


def make_form_response():
    return HtmlResponse(url=URL, body=FORM_HTML, encoding="utf-8")


def period(request):
    body = request.body.decode()
    return body.split("txtDtPeriodo=")[1].split("&")[0].replace("%2F", "/")


def http_error_failure(request, status=500):
    response = HtmlResponse(url=request.url, status=status, request=request)
    failure = Failure(HttpError(response))
    failure.request = request
    return failure


def test_start_requests_the_search_page():
    spider = MunicipioOnlineSpiderForTest()

    async def collect():
        return [request async for request in spider.start()]

    requests = asyncio.run(collect())

    assert len(requests) == 1
    assert requests[0].url == URL


def test_date_filter_request_uses_yearly_windows():
    spider = MunicipioOnlineSpiderForTest(end="2025-06-01")

    requests = list(spider.date_filter_request(make_form_response()))

    assert [period(r) for r in requests] == [
        "10/03/2024-01/01/2025",
        "01/01/2025-01/06/2025",
    ]
    assert all(r.errback == spider.split_failed_interval for r in requests)


def test_failed_interval_is_split_in_half():
    spider = MunicipioOnlineSpiderForTest()
    failed = spider.interval_request(
        make_form_response(), date(2024, 1, 1), date(2024, 12, 31)
    )

    requests = list(spider.split_failed_interval(http_error_failure(failed)))

    assert [period(r) for r in requests] == [
        "01/01/2024-01/07/2024",
        "02/07/2024-31/12/2024",
    ]
    assert requests[0].meta["interval"] == (date(2024, 1, 1), date(2024, 7, 1))


def test_failed_single_day_is_not_split():
    spider = MunicipioOnlineSpiderForTest()
    failed = spider.interval_request(
        make_form_response(), date(2024, 11, 30), date(2024, 11, 30)
    )

    assert list(spider.split_failed_interval(http_error_failure(failed))) == []


def test_non_http_errors_are_not_split():
    spider = MunicipioOnlineSpiderForTest()
    failed = Request(URL, meta={"interval": (date(2024, 1, 1), date(2024, 12, 31))})
    failure = Failure(ValueError("boom"))
    failure.request = failed

    assert list(spider.split_failed_interval(failure) or []) == []
