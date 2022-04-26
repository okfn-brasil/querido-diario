from datetime import datetime, timedelta

from spidermon import Monitor, MonitorSuite, monitors
from spidermon.contrib.actions.telegram import SendTelegramMessage
from spidermon.contrib.scrapy.monitors import (
    ErrorCountMonitor,
    FinishReasonMonitor,
    ItemValidationMonitor,
)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from gazette.extensions import JobStats


@monitors.name("Requests/Items Ratio")
class RequestsItemsRatioMonitor(Monitor):
    @monitors.name("Ratio of requests over items scraped count")
    def test_requests_items_ratio(self):
        n_scraped_items = self.data.stats.get("item_scraped_count", 0)
        n_requests_count = self.data.stats.get("downloader/request_count", 0)
        max_ratio = self.data.crawler.settings.get(
            "QUERIDODIARIO_MAX_REQUESTS_ITEMS_RATIO", 5
        )

        if n_scraped_items > 0:
            ratio = n_requests_count / n_scraped_items
            percent = round(ratio * 100, 2)
            allowed_percent = round(max_ratio * 100, 2)
            self.assertLess(
                ratio,
                max_ratio,
                msg=f"""{percent}% is greater than the allowed {allowed_percent}%
                ratio of requests over items scraped.
                """,
            )


@monitors.name("Comparison Between Executions")
class ComparisonBetweenSpiderExecutionsMonitor(Monitor):
    def _get_session(self):
        database_url = self.data.crawler.settings.get("QUERIDODIARIO_DATABASE_URL")
        engine = create_engine(database_url)
        Session = sessionmaker(bind=engine)
        return Session()

    @monitors.name("Days without gazettes")
    def test_days_without_gazettes(self):
        max_days_without_gazettes = self.data.crawler.settings.getint(
            "QUERIDODIARIO_MAX_DAYS_WITHOUT_GAZETTES"
        )
        if max_days_without_gazettes:
            session = self._get_session()
            reference_date = (
                datetime.today() - timedelta(days=max_days_without_gazettes)
            ).replace(hour=0, minute=0)

            job_stats = (
                session.query(JobStats)
                .filter(JobStats.start_time >= reference_date)
                .filter(JobStats.spider == self.data.spider.name)
                .all()
            )
            extracted_in_period = sum(
                [stat.job_stats.get("item_scraped_count", 0) for stat in job_stats]
            )
            self.assertNotEqual(
                extracted_in_period,
                0,
                msg=f"No gazettes scraped in the last {max_days_without_gazettes} days.",
            )


class CustomSendTelegramMessage(SendTelegramMessage):
    def get_message(self):
        stats = self.data.stats
        n_scraped_items = stats.get("item_scraped_count", 0)

        failures = len(self.result.failures)
        emoji = "\U0001F525" if failures > 0 else "\U0001F60E"

        message = "\n".join(
            [
                f"*{self.data.spider.name}* {stats['finish_reason']}",
                f"- Finish time: *{stats['finish_time']}*",
                f"- Gazettes scraped: *{n_scraped_items}*",
                f"- {emoji} {failures} failures {emoji}",
            ]
        )
        return message


class SpiderCloseMonitorSuite(MonitorSuite):

    monitors = [
        ComparisonBetweenSpiderExecutionsMonitor,
        RequestsItemsRatioMonitor,
        ErrorCountMonitor,
        FinishReasonMonitor,
        ItemValidationMonitor,
    ]

    monitors_failed_actions = [CustomSendTelegramMessage]
