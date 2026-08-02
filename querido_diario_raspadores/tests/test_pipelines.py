from scrapy import Spider
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
