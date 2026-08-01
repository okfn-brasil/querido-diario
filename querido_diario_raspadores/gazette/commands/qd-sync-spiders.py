"""Register spiders and their territory mapping in the platform.

This command replaces the side effect that ``initialize_database()`` used to
have when spiders opened in production: registering new/modified spiders in
the ``querido_diario_spiders`` table (and their ``territory_spider_map``).

It MUST be executed after deploying new spiders, otherwise they will never
show up as schedulable in production.

Usage:
    scrapy qd-sync-spiders

Configuration:
    - QUERIDODIARIO_API_URL / QUERIDODIARIO_API_KEY: sync through the
      Querido Diario API (POST /api/scraper/spiders/sync) — preferred;
    - QUERIDODIARIO_DATABASE_URL: fallback with direct database access
      (also initializes tables and territories, as before).
"""

from scrapy.commands import ScrapyCommand
from scrapy.exceptions import UsageError

from gazette.database.models import initialize_database
from gazette.utils.api_client import api_client_from_settings
from gazette.utils.database import generate_territory_spider_map


class Command(ScrapyCommand):
    requires_project = True

    def short_desc(self):
        return (
            "Register spiders/territories in the platform "
            "(run after deploying new spiders)"
        )

    def run(self, args, opts):
        territory_spider_map = generate_territory_spider_map()
        print(f"Found {len(territory_spider_map)} spiders in the project.")

        client = api_client_from_settings(self.settings)
        if client is not None:
            result = client.sync_spiders(territory_spider_map)
            print(f"Spiders synced through the API: {result}")
            return

        database_url = self.settings.get("QUERIDODIARIO_DATABASE_URL")
        if not database_url:
            raise UsageError(
                "Neither QUERIDODIARIO_API_URL nor QUERIDODIARIO_DATABASE_URL "
                "is set. Configure one of them to sync spiders."
            )

        initialize_database(database_url, territory_spider_map)
        print(f"Spiders synced through direct database access: {database_url}")
