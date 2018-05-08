BOT_NAME = 'gazette'
SPIDER_MODULES = ['gazette.spiders']
NEWSPIDER_MODULE = 'gazette.spiders'
ROBOTSTXT_OBEY = False
ITEM_PIPELINES = {
    'scrapy.pipelines.files.FilesPipeline': 1,
    'gazette.pipelines.PdfParsingPipeline': 2,
    'gazette.pipelines.PostgreSQLPipeline': 3,
}
FILES_STORE = '/mnt/data/'
