from types import SimpleNamespace

from scrapy import Request, Spider
from scrapy.utils.reactor import install_reactor
from scrapy.utils.test import get_crawler

from gazette.pipelines import QueridoDiarioFilesPipeline


def test_files_pipeline_can_be_created_from_crawler(tmp_path):
    install_reactor("twisted.internet.asyncioreactor.AsyncioSelectorReactor")
    crawler = get_crawler(
        Spider,
        settings_dict={
            "FILES_STORE": str(tmp_path),
            "FILES_REQUESTS_FIELD": "custom_file_requests",
        },
    )

    pipeline = QueridoDiarioFilesPipeline.from_crawler(crawler)

    assert pipeline.files_requests_field == "custom_file_requests"
    assert pipeline.secondary_bucket == ""
    assert pipeline.s3_client is None


def test_files_pipeline_allows_file_urls_from_external_domains(tmp_path):
    crawler = get_crawler(
        Spider,
        settings_dict={"FILES_STORE": str(tmp_path)},
    )
    pipeline = QueridoDiarioFilesPipeline.from_crawler(crawler)
    spider = Spider(name="test", allowed_domains=["example.com"])

    requests = list(
        pipeline.get_media_requests(
            {"file_urls": ["https://files.example.net/gazette.pdf"]},
            SimpleNamespace(spider=spider),
        )
    )

    assert len(requests) == 1
    assert requests[0].meta["allow_offsite"] is True


def test_files_pipeline_allows_file_requests_without_losing_metadata(tmp_path):
    crawler = get_crawler(
        Spider,
        settings_dict={"FILES_STORE": str(tmp_path)},
    )
    pipeline = QueridoDiarioFilesPipeline.from_crawler(crawler)
    spider = Spider(name="test", allowed_domains=["example.com"])
    file_request = Request(
        "https://files.example.net/gazette.pdf",
        meta={"document_id": "123"},
    )

    requests = list(
        pipeline.get_media_requests(
            {"file_requests": [file_request]},
            SimpleNamespace(spider=spider),
        )
    )

    assert len(requests) == 1
    assert requests[0].meta == {
        "document_id": "123",
        "allow_offsite": True,
    }
    assert "allow_offsite" not in file_request.meta
