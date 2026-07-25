from decouple import config

BOT_NAME = "gazette"
SPIDER_MODULES = ["gazette.spiders"]
NEWSPIDER_MODULE = "gazette.spiders"
ROBOTSTXT_OBEY = False
ITEM_PIPELINES = {
    "gazette.pipelines.GazetteDateFilteringPipeline": 100,
    "gazette.pipelines.DefaultValuesPipeline": 200,
    "gazette.pipelines.QueridoDiarioFilesPipeline": 300,
    "spidermon.contrib.scrapy.pipelines.ItemValidationPipeline": 400,
    # ApiPipeline persists gazettes through the Querido Diário API when
    # QUERIDODIARIO_API_URL is set; otherwise it is a no-op and
    # SQLDatabasePipeline keeps the direct database behavior (local dev).
    "gazette.pipelines.ApiPipeline": 500,
    "gazette.pipelines.SQLDatabasePipeline": 510,
}
USER_AGENT = (
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0"
)

TEMPLATES_DIR = "templates"

DOWNLOAD_TIMEOUT = 360

FILES_STORE = config("FILES_STORE", default="data")
FILES_STORE_SECONDARY = config("FILES_STORE_SECONDARY", default="")
MEDIA_ALLOW_REDIRECTS = True

EXTENSIONS = {
    "spidermon.contrib.scrapy.extensions.Spidermon": 500,
    "gazette.extensions.StatsPersist": 600,
}
SPIDERMON_ENABLED = config("SPIDERMON_ENABLED", default=True, cast=bool)
SPIDERMON_VALIDATION_SCHEMAS = ["gazette.schema.GAZETTE_SCHEMA"]

SPIDERMON_VALIDATION_ADD_ERRORS_TO_ITEMS = True
SPIDERMON_VALIDATION_DROP_ITEMS_WITH_ERRORS = True
SPIDERMON_SPIDER_CLOSE_MONITORS = ("gazette.monitors.SpiderCloseMonitorSuite",)
SPIDERMON_MAX_ERRORS = 0
SPIDERMON_MAX_ITEM_VALIDATION_ERRORS = 0

SPIDERMON_DISCORD_FAKE = config("SPIDERMON_DISCORD_FAKE", default=True, cast=bool)
SPIDERMON_DISCORD_WEBHOOK_URL = config(
    "SPIDERMON_DISCORD_WEBHOOK_URL", default="<DISCORD_WEBHOOK_URL>"
)

QUERIDODIARIO_DATABASE_URL = config(
    "QUERIDODIARIO_DATABASE_URL", default="sqlite:///querido-diario.db"
)
# When set, gazettes/job stats are persisted through the Querido Diário API
# instead of direct database access (see ApiPipeline and StatsPersist)
QUERIDODIARIO_API_URL = config("QUERIDODIARIO_API_URL", default="")
QUERIDODIARIO_API_KEY = config("QUERIDODIARIO_API_KEY", default="")
QUERIDODIARIO_MAX_REQUESTS_ITEMS_RATIO = 5
QUERIDODIARIO_MAX_DAYS_WITHOUT_GAZETTES = 7

# These settings are needed only when storing downloaded files
# in a S3 bucket
AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID", default="")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY", default="")
AWS_ENDPOINT_URL = config("AWS_ENDPOINT_URL", default="")
AWS_REGION_NAME = config("AWS_REGION_NAME", default="")
FILES_STORE_S3_ACL = config("FILES_STORE_S3_ACL", default="")

DOWNLOADER_MIDDLEWARES = {
    "gazette.middlewares.ZyteSmartProxyMiddleware": 610,
    # Detects when a response is actually a Cloudflare Turnstile challenge
    # page and fails the request/spider instead of treating it as valid
    # content (see gazette/utils/blocking.py).
    "gazette.middlewares.GazetteDownloaderMiddleware": 620,
}
ZYTE_SMARTPROXY_APIKEY = "<SMARTPROXY_APIKEY>"

COMMANDS_MODULE = "gazette.commands"

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
