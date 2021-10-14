import scrapy


class TmpSettingsSpider(scrapy.Spider):

    name = "tmp_settings"

    custom_settings = {
        "SPIDERMON_ENABLED": False,
        "ITEM_PIPELINES": {},
    }

    def start_requests(self):
        keys_of_interest = [
            "AWS_ACCESS_KEY_ID",
            "AWS_ENDPOINT_URL",
            "AWS_REGION_NAME",
            "AWS_SECRET_ACCESS_KEY",
            "FILES_STORE",
            "NAMESPACE",
            "PASSWORD",
            "QUERIDODIARIO_DATABASE_URL",
            "SCRAPY_CLOUD_PROJECT_ID",
            "SHUB_APIKEY",
            "SPIDERMON_TELEGRAM_FAKE",
            "SPIDERMON_TELEGRAM_RECIPIENTS",
            "SPIDERMON_TELEGRAM_SENDER_TOKEN",
            "USERNAME",
        ]
        for key, value in self.settings.attributes.items():
            if key in keys_of_interest:
                self.logger.info(f"{key}={value.value}")
        yield scrapy.Request("https://ok.org.br/projetos/querido-diario/")

    def parse(self, response):
        ...
