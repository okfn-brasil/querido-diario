BOT_NAME = "gazette"
SPIDER_MODULES = ["gazette.spiders"]
NEWSPIDER_MODULE = "gazette.spiders"
ROBOTSTXT_OBEY = False
ITEM_PIPELINES = {
    "gazette.pipelines.GazetteDateFilteringPipeline": 50,
    "gazette.parser.GazetteFilesPipeline": 60,
    "scrapy.pipelines.files.FilesPipeline": 100,
    "gazette.pipelines.ExtractTextPipeline": 200,
    "gazette.pipelines.PostgreSQLPipeline": 300,
    "gazette.pipelines.KafkaExporterPipeline": 400,
}
FILES_STORE = "/mnt/data/"
KAFKA_TOPIC = "gazettes"
KAFKA_HOSTS = ["kafka:9092"]
