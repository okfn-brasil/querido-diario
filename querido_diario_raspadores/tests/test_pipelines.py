from datetime import date
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
from scrapy import Request, Spider
from scrapy.exceptions import DropItem
from scrapy.http import Response
from scrapy.pipelines.media import MediaPipeline
from scrapy.utils.reactor import install_reactor
from scrapy.utils.test import get_crawler

from gazette.pipelines import (
    ApiPipeline,
    DefaultValuesPipeline,
    GazetteDateFilteringPipeline,
    QueridoDiarioFilesPipeline,
    SQLDatabasePipeline,
)


def test_date_filtering_pipeline_uses_spider_from_crawler():
    spider = SimpleNamespace(start_date=date(2026, 1, 2))
    pipeline = GazetteDateFilteringPipeline.from_crawler(SimpleNamespace(spider=spider))
    accepted_item = {"date": date(2026, 1, 2)}

    assert pipeline.process_item(accepted_item) is accepted_item

    with pytest.raises(DropItem):
        pipeline.process_item({"date": date(2026, 1, 1)})


def test_default_values_pipeline_uses_spider_from_crawler():
    crawler = SimpleNamespace(spider=SimpleNamespace(TERRITORY_ID="1234567"))
    pipeline = DefaultValuesPipeline.from_crawler(crawler)
    item = {"date": date(2026, 1, 1)}

    result = pipeline.process_item(item)

    assert result["territory_id"] == "1234567"
    assert result["date"] == "2026-01-01"
    assert result["scraped_at"].endswith("Z")


def test_api_pipeline_is_noop_without_api_configuration():
    crawler = SimpleNamespace(settings={}, spider=SimpleNamespace())
    pipeline = ApiPipeline.from_crawler(crawler)
    item = {"date": "2026-01-01"}

    pipeline.open_spider()

    assert pipeline.process_item(item) is item


def test_database_pipeline_is_noop_without_database_configuration():
    crawler = SimpleNamespace(settings={}, spider=SimpleNamespace())
    pipeline = SQLDatabasePipeline.from_crawler(crawler)
    item = {"date": "2026-01-01"}

    pipeline.open_spider()

    assert pipeline.process_item(item) is item


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


def build_files_pipeline_with_secondary_bucket(tmp_path, **extra_settings):
    install_reactor("twisted.internet.asyncioreactor.AsyncioSelectorReactor")
    crawler = get_crawler(
        Spider,
        settings_dict={
            "FILES_STORE": str(tmp_path),
            "FILES_STORE_SECONDARY": "s3://secondary-bucket/",
            "AWS_REGION_NAME": "us-east-1",
            **extra_settings,
        },
    )
    pipeline = QueridoDiarioFilesPipeline.from_crawler(crawler)
    pipeline.s3_client = MagicMock()
    return pipeline, MediaPipeline.SpiderInfo(Spider(name="test"))


def download_gazette_file(pipeline, info):
    request = Request("https://example.com/diario.pdf")
    response = Response(
        request.url,
        body=b"%PDF-1.4 gazette",
        headers={"Content-Type": "application/pdf"},
        request=request,
    )
    item = {"territory_id": "1234567", "date": "2026-01-01"}
    return pipeline.media_downloaded(response, request, info, item=item)


def test_files_pipeline_copies_file_to_secondary_bucket(tmp_path):
    pipeline, info = build_files_pipeline_with_secondary_bucket(tmp_path)

    result = download_gazette_file(pipeline, info)

    assert result["status"] == "downloaded"
    assert result["path"].startswith("1234567/2026-01-01/")
    assert result["path"].endswith(".pdf")
    assert (tmp_path / result["path"]).read_bytes() == b"%PDF-1.4 gazette"
    pipeline.s3_client.put_object.assert_called_once_with(
        Bucket="secondary-bucket",
        Key=result["path"],
        Body=b"%PDF-1.4 gazette",
        ACL="private",
    )


def test_files_pipeline_uses_configured_acl_in_secondary_bucket(tmp_path):
    pipeline, info = build_files_pipeline_with_secondary_bucket(
        tmp_path, FILES_STORE_S3_ACL="public-read"
    )

    download_gazette_file(pipeline, info)

    assert pipeline.s3_client.put_object.call_args.kwargs["ACL"] == "public-read"


def test_files_pipeline_keeps_file_when_secondary_bucket_copy_fails(tmp_path):
    pipeline, info = build_files_pipeline_with_secondary_bucket(tmp_path)
    pipeline.s3_client.put_object.side_effect = Exception("bucket unavailable")

    result = download_gazette_file(pipeline, info)

    assert result["status"] == "downloaded"
    assert (tmp_path / result["path"]).exists()
