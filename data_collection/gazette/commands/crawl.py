import logging
from functools import lru_cache

from scrapy.commands.crawl import Command as CrawlCommand
from scrapy.exceptions import UsageError

from gazette.exceptions import WrongTimespan

logger = logging.getLogger(__name__)


class Command(CrawlCommand):
    def run(self, args, opts):
        if len(args) < 1:
            raise UsageError()
        elif len(args) > 1:
            raise UsageError(
                "running 'scrapy crawl' with more than one spider as argument is not supported"
            )
        spidername = args[0]

        if self._has_multiple_sources(spidername):
            logger.info(
                "Multiple sources were detected for this spider name. Running all possibilities with the given timespan..."
            )
            for source in self._sources_spidernames(spidername):
                if not self._is_timespan_available(source, opts.spargs):
                    continue

                self._defer_crawl(source, opts.spargs)
        else:
            self._defer_crawl(spidername, opts.spargs)

        if self.exitcode != 1:
            self.crawler_process.start()

            if (
                self.crawler_process.bootstrap_failed
                or hasattr(self.crawler_process, "has_exception")
                and self.crawler_process.has_exception
            ):
                self.exitcode = 1

    def _has_multiple_sources(self, name):
        return len(self._sources_spidernames(name)) > 1

    @lru_cache
    def _sources_spidernames(self, name):
        sources = [
            s for s in self.crawler_process.spider_loader._spiders.keys() if name in s
        ]
        return sorted(sources)

    def _is_timespan_available(self, spidername, kwargs={}):
        spiderclass = self._class_from_spidername(spidername)
        try:
            spiderclass(**kwargs)
        except WrongTimespan:
            logger.info(f"The given timespan doesn't apply to the {spidername} spider.")
            return False
        return True

    def _class_from_spidername(self, spidername):
        return self.crawler_process.spider_loader._spiders[spidername]

    def _defer_crawl(self, spidername, kwargs={}):
        crawl_defer = self.crawler_process.crawl(spidername, **kwargs)
        result = getattr(crawl_defer, "result", None)
        if self._crawl_failed(result):
            self.exitcode = 1

    def _crawl_failed(self, deferred_result):
        return deferred_result is not None and issubclass(
            deferred_result.type, Exception
        )
