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
                start = datetime.date.fromisoformat(opts.start)
            except ValueError:
                raise UsageError("'start' must match YYYY-MM-DD format")

        if opts.end is not None:
            try:
                end = datetime.date.fromisoformat(opts.end)
            except ValueError:
                raise UsageError("'end' must match YYYY-MM-DD format")

        print("\nEnabled spiders\n===============")
        for spider_name in get_enabled_spiders(
            database_url=self.settings["QUERIDODIARIO_DATABASE_URL"],
            api_url=self.settings.get("QUERIDODIARIO_API_URL"),
            api_key=self.settings.get("QUERIDODIARIO_API_KEY"),
            start_date=start,
            end_date=end,
        ):
            print(spider_name)
