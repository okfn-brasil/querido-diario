from collections import namedtuple
from datetime import datetime
from itertools import pairwise

from dateutil.rrule import DAILY, MONTHLY, WEEKLY, YEARLY, rrule, rruleset

YearMonthDate = namedtuple("YearMonthDate", ["year", "month"])
DateRange = namedtuple("DateRange", ["start", "end"])


def daily_sequence(start, end, format=None):
    """Return a list of days, everyday, between start and end"""
    return generate_dates_sequence(start, end, DAILY, format=format)


def monthly_sequence(start, end, format=None):
    """Return a list of months, every month, between start and end.

    This func should be used when days doesnt matter, only month <> year pair are necessary

    Default return is a list of YearMonthDate, like [(year, month),...,(year, month)]
    If a date format is given, return a list of date strings

    E.g.: range (2025, 10, 15) to (2025, 12, 15)
    output:
        [   YearMonthDate(2025, 10),
            YearMonthDate(2025, 11),
            YearMonthDate(2025, 12),
        ]
    formatted output:
        [   "2025/10",
            "2025/11",
            "2025/12"
        ]
    """
    start = datetime(start.year, start.month, 1)

    if format:
        months = generate_dates_sequence(
            start, end, MONTHLY, bymonthday=1, format=format
        )
    else:
        months = generate_dates_sequence(start, end, MONTHLY, bymonthday=1)
        months = [YearMonthDate(year=x.year, month=x.month) for x in months]

    return months


def yearly_sequence(start, end, format=None):
    """Return a list of years, every year, between start and end.

    This func should be used when days and months doesnt matter, only year is necessary

    Default return is a list of int, like [year, ... , year]
    If a date format is given, return a list of date strings

    E.g.: range (2022, 10, 15) to (2024, 12, 15)
    output:
        [   2022,
            2023,
            2024,
        ]
    formatted output:
        [   "2022",
            "2023",
            "2024"
        ]
    """
    start = datetime(start.year, 1, 1)

    if format:
        years = generate_dates_sequence(
            start, end, YEARLY, bymonth=1, bymonthday=1, format=format
        )
    else:
        years = generate_dates_sequence(start, end, YEARLY, bymonth=1, bymonthday=1)
        years = [x.year for x in years]

    return years


def weekly_window(start, end, format=None):
    """Return a list of DateRange(start, end) objects with weekly intervals,
    between start and end.

    start and end are, by default, datetime
    but if format is given, start and end become strings

    E.g: range (2022, 3, 10) to (2022, 3, 20)
    output:
        [   DateRange(datetime(2022, 3, 10), datetime(2022, 3, 17)),
            DateRange(datetime(2022, 3, 17), datetime(2022, 3, 20)),
        ]
    formatted output:
        [   DateRange("2022-03-10", "2022-03-17"),
            DateRange("2022-03-17", "2022-03-20"),
        ]
    """
    return __make_daterange_list(
        generate_dates_sequence(start, end, WEEKLY, end_included=True, format=format)
    )


def monthly_window(start, end, format=None):
    """Return a list of DateRange(start, end) objects with intervals by months
    1th day, between start and end.

    start and end are, by default, datetime
    but if format is given, start and end become strings

    E.g: range (2022, 3, 10) to (2022, 5, 29)
    output:
        [   DateRange(datetime(2022, 3, 10), datetime(2022, 4, 1)),
            DateRange(datetime(2022, 4, 1), datetime(2022, 5, 1)),
            DateRange(datetime(2022, 5, 1), datetime(2022, 5, 29)),
        ]
    formatted output:
        [   DateRange("2022-03-10", "2022-04-01"),
            DateRange("2022-04-01", "2022-05-01"),
            DateRange("2022-05-01", "2022-05-29")
        ]
    """
    return __make_daterange_list(
        generate_dates_sequence(
            start, end, MONTHLY, bymonthday=1, end_included=True, format=format
        )
    )


def yearly_window(start, end, format=None):
    """Return a list of DateRange(start, end) objects with intervals by years
    1th day, between start and end.

    start and end are, by default, datetime
    but if format is given, start and end become strings

    E.g: range (2022, 3, 10) to (2024, 2, 3)
    output:
        [   DateRange(datetime(2022, 3, 10), datetime(2023, 1, 1)),
            DateRange(datetime(2023, 1, 1), datetime(2024, 1, 1)),
            DateRange(datetime(2024, 1, 1), datetime(2024, 2, 3)),
        ]
    formatted output:
        [   DateRange("2022-03-10", "2023-01-01"),
            DateRange("2023-01-01", "2024-01-01"),
            DateRange("2024-01-01", "2024-02-03")
        ]
    """
    return __make_daterange_list(
        generate_dates_sequence(
            start,
            end,
            YEARLY,
            bymonth=1,
            bymonthday=1,
            end_included=True,
            format=format,
        )
    )


def generate_dates_sequence(
    start,
    end,
    recurrence,
    bymonth=None,
    bymonthday=None,
    end_included=False,
    format=False,
):
    start = datetime(start.year, start.month, start.day)
    end = datetime(end.year, end.month, end.day)

    dates = rruleset()
    dates.rdate(start)
    dates.rrule(
        rrule(
            recurrence,
            dtstart=start,
            until=end,
            bymonth=bymonth,
            bymonthday=bymonthday,
        )
    )

    if end_included:
        dates.rdate(end)

        if start == end:
            dates = [start, end]

    if format:
        dates = [x.strftime(format) for x in dates]
    else:
        dates = list(dates)

    return dates


def __make_daterange_list(dates):
    paired_dates = [DateRange(element[0], element[1]) for element in pairwise(dates)]
    return paired_dates
