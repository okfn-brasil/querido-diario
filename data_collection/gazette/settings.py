import pkg_resources

BOT_NAME = "gazette"
SPIDER_MODULES = ["gazette.spiders"]
NEWSPIDER_MODULE = "gazette.spiders"
ROBOTSTXT_OBEY = False
ITEM_PIPELINES = {
    "gazette.pipelines.GazetteDateFilteringPipeline": 100,
    "gazette.pipelines.DefaultValuesPipeline": 200,
    "gazette.pipelines.QueridoDiarioFilesPipeline": 300,
    "spidermon.contrib.scrapy.pipelines.ItemValidationPipeline": 400,
    "gazette.pipelines.SQLDatabasePipeline": 500,
    "gazette.pipelines.AmqpExporterPipeline": 500,
    "gazette.pipelines.KafkaExporterPipeline": 500,
    "gazette.pipelines.SQSExporterPipeline": 500,
    "gazette.pipelines.KinesisExporterPipeline": 500,
}

DOWNLOAD_TIMEOUT = 360

FILES_STORE = "data"
MEDIA_ALLOW_REDIRECTS = True

EXTENSIONS = {
    "spidermon.contrib.scrapy.extensions.Spidermon": 500,
    "gazette.extensions.StatsPersist": 600,
}
SPIDERMON_ENABLED = True
SPIDERMON_VALIDATION_SCHEMAS = [
    pkg_resources.resource_filename("gazette", "resources/gazette_schema.json")
]

SPIDERMON_VALIDATION_ADD_ERRORS_TO_ITEMS = True
SPIDERMON_VALIDATION_DROP_ITEMS_WITH_ERRORS = True
SPIDERMON_SPIDER_CLOSE_MONITORS = ("gazette.monitors.SpiderCloseMonitorSuite",)
SPIDERMON_MAX_ERRORS = 0

SPIDERMON_TELEGRAM_FAKE = True
SPIDERMON_TELEGRAM_SENDER_TOKEN = "<TELEGRAM_BOT_TOKEN>"
SPIDERMON_TELEGRAM_RECIPIENTS = ["<RECIPIENT>"]

QUERIDODIARIO_DATABASE_URL = "sqlite:///querido-diario.db"
QUERIDODIARIO_MAX_REQUESTS_ITEMS_RATIO = 5
QUERIDODIARIO_MAX_DAYS_WITHOUT_GAZETTES = 5

# These settings are used when storing downloaded files
# in a S3 bucket and to integrate with other AWS services
AWS_ACCESS_KEY_ID = ""
AWS_SECRET_ACCESS_KEY = ""
AWS_REGION_NAME = ""
AWS_ENDPOINT_URL = ""
FILES_STORE_S3_ACL = "public-read"

# AMQP exporter pipeline
AMQP_HOST = "localhost:5672"
AMQP_USERNAME = "guest"
AMQP_PASSWORD = "guest"
AMQP_QUEUE = "querido-diario"
AMQP_EXCHANGE = ""
AMQP_ROUTING_KEY = "querido-diario"

# Kafka exporter pipeline
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
KAFKA_TOPIC = "querido-diario"

# SQS exporter pipeline
SQS_QUEUE_NAME = "querido-diario"

# Kinesis exporter pipeline
KINESIS_STREAM_NAME = "querido-diario"
