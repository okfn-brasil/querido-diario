import datetime

from scrapy.commands import ScrapyCommand
from scrapy.exceptions import UsageError

from gazette.utils.database import get_enabled_spiders


class Command(ScrapyCommand):
    requires_project = True

    def add_options(self, parser):
        ScrapyCommand.add_options(self, parser)
        parser.add_argument(
            "--start",
            dest="start",
            default=None,
            metavar="VALUE",
            help="List spiders enabled from date (format: YYYY-MM-DD)",
        )
        parser.add_argument(
            "--end",
            dest="end",
            default=None,
            metavar="VALUE",
            help="List spiders enabled until date (format: YYYY-MM-DD)",
        )

    def short_desc(self):
        return "List production enabled spiders"

    def run(self, args, opts):
        start, end = None, None

        if opts.start is not None:
            try:
                start = datetime.datetime.strptime(opts.start, "%Y-%m-%d")
            except ValueError:
                raise UsageError("'start' must match YYYY-MM-DD format")

        if opts.end is not None:
            try:
                end = datetime.datetime.strptime(opts.end, "%Y-%m-%d")
            except ValueError:
                raise UsageError("'end' must match YYYY-MM-DD format")

        print("\nEnabled spiders\n===============")
        for spider_name in get_enabled_spiders(
            database_url=self.settings["QUERIDODIARIO_DATABASE_URL"],
            start_date=start,
            end_date=end,
        ):
            print(spider_name)
