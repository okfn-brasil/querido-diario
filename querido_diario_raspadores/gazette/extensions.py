import json
import os

import requests
from scrapy import signals
from scrapy.exceptions import NotConfigured

from gazette.utils.api_client import api_client_from_settings


class StatsPersist:
    """Persist the Scrapy stats of a finished job through the API.

    Disabled (NotConfigured) when QUERIDODIARIO_API_URL is not set,
    keeping local development free of external dependencies.
    """

    def __init__(self, crawler, client):
        self._stats = crawler.stats
        self._client = client

    @classmethod
    def from_crawler(cls, crawler):
        client = api_client_from_settings(crawler.settings)
        if client is None:
            raise NotConfigured(
                "QUERIDODIARIO_API_URL is not set. StatsPersist disabled."
            )

        o = cls(crawler, client)
        crawler.signals.connect(o.spider_closed, signal=signals.spider_closed)
        return o

    def spider_closed(self, spider, reason):
        stats = self._stats.get_stats()
        serializable_stats = json.loads(json.dumps(stats, default=str))
        try:
            self._client.post_job_stats(
                spider_name=spider.name,
                job_id=os.environ.get("SHUB_JOBKEY", ""),
                stats_dict=serializable_stats,
            )
        except requests.RequestException as exc:
            spider.logger.warning(
                f"Something wrong has happened when sending job stats to the API. "
                f"Details: {exc}"
            )
