"""Run a spider and generate its output, a log file and metrics for evaluation."""
import json
from datetime import datetime
from pathlib import Path

from scrapy.commands import BaseRunSpiderCommand
from scrapy.exceptions import UsageError


def print_metrics(spider_name: str, output_filename: list, args: dict = {}):
    print(f"------------------- {spider_name} stats -------------------")
    output_filepath = Path(".") / output_filename[0]
    print("Output:", output_filepath.resolve())
    print("Args:", args)
    dates = []
    lines = output_filepath.read_text().splitlines()
    for line in lines:
        gazette = json.loads(line)
        dates.append(datetime.strptime(gazette["date"], "%Y-%m-%d").date())
    sorted_dates = sorted(dates)
    print("\n")
    total = len(lines)
    print(f"Total of gazettes: {total}")
    start_date = sorted_dates[0]
    end_date = sorted_dates[-1]
    print(f"First date: {start_date} \nLast date: {end_date}")
    delta = end_date - start_date
    print(f"Average of gazettes per day ({delta.days} days): {total/delta.days:.1f}")
    diff_years = end_date.year - start_date.year
    if diff_years:
        diff_months = diff_years * 12 + end_date.month - start_date.month
        print(
            f"Average of gazettes by month ({diff_months} months): {total/diff_months:.1f}"
        )
        print(
            f"Average of gazettes by year ({diff_years} years): {total/diff_years:.1f}"
        )


class Command(BaseRunSpiderCommand):

    requires_project = True
    default_settings = {"FILES_STORE": ""}

    def syntax(self):
        return "[options] <spider>"

    def short_desc(self):
        return "Run a spider and print metrics for review"

    def add_options(self, parser):
        BaseRunSpiderCommand.add_options(self, parser)
        parser.add_option(
            "--skip-execution",
            action="store_true",
            help="skip spider execution and print metrics",
        )

    def process_options(self, args, options):
        spider_name = args[0]
        if not options.logfile:
            options.logfile = f"{spider_name}.log"
        if not options.output:
            options.output = [f"{spider_name}.jsonlines"]

        BaseRunSpiderCommand.process_options(self, args, options)

    def run(self, args, options):
        if len(args) < 1:
            raise UsageError()
        elif len(args) > 1:
            raise UsageError(
                "running 'scrapy crawl' with more than one spider is not supported"
            )
        spider_name = args[0]

        crawl_defer = self.crawler_process.crawl(spider_name, **options.spargs)

        has_result = hasattr(crawl_defer, "result")
        failed = all(
            [
                has_result and getattr(crawl_defer, "result") is not None,
                has_result and issubclass(crawl_defer.result.type, Exception),
            ]
        )
        if failed:
            self.exitcode = 1
        else:
            if not options.skip_execution:
                self.crawler_process.start()

            has_exception_attr = hasattr(self.crawler_process, "has_exception")
            failed = any(
                [
                    self.crawler_process.bootstrap_failed,
                    has_exception_attr and self.crawler_process.has_exception,
                ]
            )

            if failed:
                self.exitcode = 1

            print_metrics(spider_name, options.output, options.spargs)
