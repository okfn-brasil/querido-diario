from scrapy.settings import Settings
from scrapy.spiderloader import SpiderLoader

from gazette import settings


def test_spiders_do_not_define_legacy_start_requests():
    loader = SpiderLoader.from_settings(
        Settings({"SPIDER_MODULES": settings.SPIDER_MODULES})
    )

    legacy_spiders = []
    for spider_name in loader.list():
        spider_class = loader.load(spider_name)
        project_classes = (
            cls for cls in spider_class.__mro__ if cls.__module__.startswith("gazette.")
        )
        if any("start_requests" in cls.__dict__ for cls in project_classes):
            legacy_spiders.append(spider_name)

    assert legacy_spiders == []
