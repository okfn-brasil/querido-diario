"""HTTP client for the Querido Diário API scraper endpoints.

Replaces the direct database access previously done by the spiders when
running in production (Zyte / Scrapy Cloud). All endpoints are authenticated
with an API Key sent in the ``X-API-Key`` header.

Configuration (environment variables or Scrapy settings):
    - ``QUERIDODIARIO_API_URL``: base URL of the API
      (e.g. ``https://queridodiario.ok.org.br/api``... base host only,
      the ``/scraper/*`` path is appended by the client)
    - ``QUERIDODIARIO_API_KEY``: API Key for the scraper endpoints
"""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

DEFAULT_TIMEOUT = 30
RETRY_TOTAL = 5
RETRY_BACKOFF_FACTOR = 2  # 2s, 4s, 8s, 16s, 32s
RETRY_STATUS_FORCELIST = [429, 500, 502, 503, 504]


class QueridoDiarioAPIClient:
    """Client for the ``/scraper/*`` endpoints of the Querido Diário API.

    Retries with exponential backoff are enabled for GET and POST requests.
    Retrying POSTs is safe because the server-side inserts are idempotent
    (``ON CONFLICT DO NOTHING`` over unique constraints).
    """

    def __init__(self, base_url, api_key, timeout=DEFAULT_TIMEOUT):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers["X-API-Key"] = api_key or ""
        retry = Retry(
            total=RETRY_TOTAL,
            backoff_factor=RETRY_BACKOFF_FACTOR,
            status_forcelist=RETRY_STATUS_FORCELIST,
            allowed_methods=["GET", "POST"],  # POST is idempotent server-side
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def _get(self, path, params=None):
        response = self.session.get(
            f"{self.base_url}{path}", params=params, timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def _post(self, path, payload):
        response = self.session.post(
            f"{self.base_url}{path}", json=payload, timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def get_enabled_spiders(self, start_date=None, end_date=None):
        """Return the names of the enabled spiders within the date period.

        GET /scraper/spiders
        """
        params = {}
        if start_date is not None:
            params["start_date"] = str(start_date)
        if end_date is not None:
            params["end_date"] = str(end_date)
        data = self._get("/scraper/spiders", params=params)
        return [spider["spider_name"] for spider in data["spiders"]]

    def post_gazette(self, gazette):
        """Persist a scraped gazette (metadata only).

        POST /scraper/gazettes

        The endpoint is idempotent: posting a duplicate
        (same territory_id + date + file_checksum) is a no-op.
        """
        return self._post("/scraper/gazettes", gazette)

    def post_job_stats(self, spider_name, job_id, stats_dict):
        """Persist the Scrapy stats of a finished job.

        POST /scraper/job-stats
        """
        payload = {
            "spider_name": spider_name,
            "job_id": job_id,
            "start_time": str(stats_dict.get("start_time", "")),
            "stats": stats_dict,
        }
        return self._post("/scraper/job-stats", payload)

    def get_job_stats(self, spider_name, since_date):
        """Return the job stats of a spider since a given date.

        GET /scraper/job-stats?spider=<name>&since=<YYYY-MM-DD>

        Returns a list of dicts, each one with at least a ``stats`` key
        holding the Scrapy stats collected for that job.
        """
        params = {"spider": spider_name, "since": str(since_date)}
        data = self._get("/scraper/job-stats", params=params)
        return data["job_stats"]

    def sync_spiders(self, territory_spider_map):
        """Register new/modified spiders and their territory mapping.

        POST /scraper/spiders/sync

        ``territory_spider_map`` is an iterable of
        ``(spider_name, territory_id, date_from)`` tuples.
        """
        payload = {
            "spiders": [
                {
                    "spider_name": spider_name,
                    "territory_id": territory_id,
                    "date_from": str(date_from),
                }
                for spider_name, territory_id, date_from in territory_spider_map
            ]
        }
        return self._post("/scraper/spiders/sync", payload)


def api_client_from_settings(settings):
    """Build a client from Scrapy settings, or return None when the API
    is not configured (local development without API access)."""
    api_url = settings.get("QUERIDODIARIO_API_URL")
    if not api_url:
        return None
    return QueridoDiarioAPIClient(api_url, settings.get("QUERIDODIARIO_API_KEY", ""))
