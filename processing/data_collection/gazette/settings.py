from decouple import config

BOT_NAME = 'gazette'
SPIDER_MODULES = ['gazette.spiders']
NEWSPIDER_MODULE = 'gazette.spiders'
ROBOTSTXT_OBEY = False
ITEM_PIPELINES = {
    'gazette.pipelines.GazetteDateFilteringPipeline': 50,
    'gazette.parser.GazetteFilesPipeline': 60,
    'scrapy.pipelines.files.FilesPipeline': 100,
    'gazette.pipelines.PdfParsingPipeline': 200,
    'gazette.pipelines.PostgreSQLPipeline': 300,
}

FILES_STORE = config('FILES_STORE', '/mnt/data/')
