import datetime

from scrapy.commands import ScrapyCommand
from scrapy.exceptions import UsageError

from gazette.utils.database import get_enabled_spiders


class Command(ScrapyCommand):
    requires_project = True

    def add_options(self, parser):
        ScrapyCommand.add_options(self, parser)
        parser.add_argument(
            "--start_date",
            dest="start_date",
            default=None,
            metavar="VALUE",
            help="List spiders enabled from date (format: YYYY-MM-DD)",
        )
        parser.add_argument(
            "--end_date",
            dest="end_date",
            default=None,
            metavar="VALUE",
            help="List spiders enabled until date (format: YYYY-MM-DD)",
        )

    def short_desc(self):
        return "List production enabled spiders"

    def run(self, args, opts):
        start_date, end_date = None, None

        if opts.start_date is not None:
            try:
                start_date = datetime.datetime.strptime(opts.start_date, "%Y-%m-%d")
            except ValueError:
                raise UsageError("'start_date' must match YYYY-MM-DD format")

        if opts.end_date is not None:
            try:
                end_date = datetime.datetime.strptime(opts.end_date, "%Y-%m-%d")
            except ValueError:
                raise UsageError("'end_date' must match YYYY-MM-DD format")

        print("\nEnabled spiders\n===============")
        for spider_name in get_enabled_spiders(
            database_url=self.settings["QUERIDODIARIO_DATABASE_URL"],
            start_date=start_date,
            end_date=end_date,
        ):
            print(spider_name)
