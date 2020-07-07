BOT_NAME = "gazette"
SPIDER_MODULES = ["gazette.spiders"]
NEWSPIDER_MODULE = "gazette.spiders"
ROBOTSTXT_OBEY = False
ITEM_PIPELINES = {
    "gazette.pipelines.GazetteDateFilteringPipeline": 50,
    "scrapy.pipelines.files.FilesPipeline": 100,
    "gazette.pipelines.ExtractTextPipeline": 200,
    "gazette.pipelines.PostgreSQLPipeline": 300,
}
SPIDER_MIDDLEWARES = {"scrapy_deltafetch.DeltaFetch": 100}
FILES_STORE = "/mnt/data/"
# skip already crawled item
DELTAFETCH_ENABLED = True
DELTAFETCH_DIR = "/mnt/data/deltafetch"
