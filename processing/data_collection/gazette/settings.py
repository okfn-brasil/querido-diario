BOT_NAME = "gazette"
SPIDER_MODULES = ["gazette.spiders"]
NEWSPIDER_MODULE = "gazette.spiders"
ROBOTSTXT_OBEY = False
ITEM_PIPELINES = {
    "gazette.pipelines.GazetteDateFilteringPipeline": 50,
    "scrapy.pipelines.files.FilesPipeline": 100,
    "gazette.pipelines.ExtractTextPipeline": 200,
}
FILES_STORE = "/mnt/data/"
