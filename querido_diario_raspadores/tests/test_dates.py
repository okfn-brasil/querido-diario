from datetime import date, datetime

from dateutil.rrule import DAILY, MONTHLY, WEEKLY, YEARLY

from gazette.utils.dates import (
    DateRange,
    YearMonthDate,
    daily_sequence,
    generate_dates_sequence,
    monthly_sequence,
    monthly_window,
    weekly_window,
    yearly_sequence,
    yearly_window,
)


class TestDailySequence:
    # DAILY
    def test_when_day_doesnt_always_exist_should_return_sequence_without_it(self):
        # no 29, 30 and 31
        assert daily_sequence(
            start=datetime(2025, 2, 28), end=datetime(2025, 3, 2)
        ) == [
            datetime(2025, 2, 28),
            datetime(2025, 3, 1),
            datetime(2025, 3, 2),
        ]

        # no 30 and 31
        assert daily_sequence(
            start=datetime(2024, 2, 28), end=datetime(2024, 3, 2), format="%Y-%m-%d"
        ) == ["2024-02-28", "2024-02-29", "2024-03-01", "2024-03-02"]

        # no 31
        assert daily_sequence(
            start=datetime(2024, 6, 28), end=datetime(2024, 7, 2), format="%d/%m/%Y"
        ) == [
            "28/06/2024",
            "29/06/2024",
            "30/06/2024",
            "01/07/2024",
            "02/07/2024",
        ]


class TestMonthlySequence:
    def test_default_return_should_be_tuple_of_date_elements(self):
        assert monthly_sequence(
            start=datetime(2025, 10, 15), end=datetime(2025, 12, 15)
        ) == [
            YearMonthDate(2025, 10),
            YearMonthDate(2025, 11),
            YearMonthDate(2025, 12),
        ]

    def test_when_format_is_given_should_return_a_list_of_date_strings(self):
        assert monthly_sequence(
            start=datetime(2025, 10, 15), end=datetime(2025, 12, 15), format="%Y/%m"
        ) == ["2025/10", "2025/11", "2025/12"]

    def test_when_startday_doesnt_exist_monthly_should_still_return_consecutive_sequence_with_them(
        self,
    ):
        # 31th doesnt exist in months 02, 04, 06, 08, 09 and 11, but those months are expected in sequence
        assert monthly_sequence(
            start=datetime(2022, 1, 31), end=datetime(2022, 12, 31)
        ) == [
            YearMonthDate(2022, 1),
            YearMonthDate(2022, 2),
            YearMonthDate(2022, 3),
            YearMonthDate(2022, 4),
            YearMonthDate(2022, 5),
            YearMonthDate(2022, 6),
            YearMonthDate(2022, 7),
            YearMonthDate(2022, 8),
            YearMonthDate(2022, 9),
            YearMonthDate(2022, 10),
            YearMonthDate(2022, 11),
            YearMonthDate(2022, 12),
        ]


class TestYearlySequence:
    def test_default_return_should_be_a_list_of_int_elements(self):
        assert yearly_sequence(
            start=datetime(2020, 12, 31), end=datetime(2025, 5, 15)
        ) == [
            2020,
            2021,
            2022,
            2023,
            2024,
            2025,
        ]

    def test_when_format_is_given_should_return_a_list_of_date_strings(self):
        assert yearly_sequence(
            start=datetime(2020, 12, 31), end=datetime(2025, 5, 15), format="%Y"
        ) == ["2020", "2021", "2022", "2023", "2024", "2025"]

    def test_when_startday_doesnt_exist_yearly_should_still_return_consecutive_sequence_with_them(
        self,
    ):
        # February 29th doesnt exist in 2025, 2026, 2027, 2029, 2030, but those years are expected in sequence
        assert yearly_sequence(
            start=datetime(2024, 2, 29), end=datetime(2030, 3, 15)
        ) == [
            2024,
            2025,
            2026,
            2027,
            2028,
            2029,
            2030,
        ]


class TestWeeklyWindow:
    def test_default_return_should_be_list_of_daterange_with_datetimes(self):
        assert weekly_window(start=datetime(2025, 1, 1), end=datetime(2025, 1, 1)) == [
            DateRange(datetime(2025, 1, 1), datetime(2025, 1, 1))
        ]

    def test_when_format_is_given_return_should_be_a_list_of_daterange_with_strings(
        self,
    ):
        assert weekly_window(
            start=datetime(2025, 1, 1), end=datetime(2025, 1, 1), format="%d-%m-%Y"
        ) == [DateRange("01-01-2025", "01-01-2025")]

    def test_when_start_to_end_range_is_less_than_interval_return_start_to_end_daterange(
        self,
    ):
        assert weekly_window(  # weekly, but start to end less than a week
            start=datetime(2022, 3, 10), end=datetime(2022, 3, 15)
        ) == [DateRange(datetime(2022, 3, 10), datetime(2022, 3, 15))]

    def test_when_enddate_greater_than_interval_return_sequence_and_residual_part(self):
        assert weekly_window(
            start=datetime(2022, 3, 10), end=datetime(2022, 3, 20)
        ) == [
            DateRange(datetime(2022, 3, 10), datetime(2022, 3, 17)),
            DateRange(datetime(2022, 3, 17), datetime(2022, 3, 20)),
        ]


class TestMonthlyWindow:
    def test_default_return_should_be_list_of_daterange_with_datetimes(self):
        assert monthly_window(start=datetime(2025, 1, 1), end=datetime(2025, 1, 1)) == [
            DateRange(datetime(2025, 1, 1), datetime(2025, 1, 1))
        ]

    def test_when_format_is_given_return_should_be_a_list_of_daterange_with_strings(
        self,
    ):
        assert monthly_window(
            start=datetime(2025, 1, 1), end=datetime(2025, 1, 1), format="%Y/%m/%d"
        ) == [DateRange("2025/01/01", "2025/01/01")]

    def test_if_windows_always_happens_using_month_day_one(self):
        # (year, month, 1)
        assert monthly_window(
            start=datetime(2022, 9, 15), end=datetime(2022, 12, 15)
        ) == [
            DateRange(datetime(2022, 9, 15), datetime(2022, 10, 1)),
            DateRange(datetime(2022, 10, 1), datetime(2022, 11, 1)),
            DateRange(datetime(2022, 11, 1), datetime(2022, 12, 1)),
            DateRange(datetime(2022, 12, 1), datetime(2022, 12, 15)),
        ]

    def test_when_start_to_end_range_is_less_than_interval_return_start_to_end_daterange(
        self,
    ):
        assert monthly_window(  # monthly, but start to end is less than a month
            start=datetime(2022, 3, 10), end=datetime(2022, 3, 15)
        ) == [DateRange(datetime(2022, 3, 10), datetime(2022, 3, 15))]

    def test_when_enddate_greater_than_interval_return_sequence_and_residual_part(self):
        assert monthly_window(
            start=datetime(2022, 10, 1), end=datetime(2022, 12, 20)
        ) == [
            DateRange(datetime(2022, 10, 1), datetime(2022, 11, 1)),
            DateRange(datetime(2022, 11, 1), datetime(2022, 12, 1)),
            DateRange(datetime(2022, 12, 1), datetime(2022, 12, 20)),
        ]


class TestYearlyyWindow:
    def test_default_return_should_be_list_of_daterange_with_datetimes(self):
        assert yearly_window(start=datetime(2025, 1, 1), end=datetime(2025, 1, 1)) == [
            DateRange(datetime(2025, 1, 1), datetime(2025, 1, 1))
        ]

    def test_when_format_is_given_return_should_be_a_list_of_daterange_with_strings(
        self,
    ):
        assert yearly_window(
            start=datetime(2025, 1, 1), end=datetime(2025, 1, 1), format="%Y%m%d"
        ) == [DateRange("20250101", "20250101")]

    def test_if_windows_always_happens_using_month_one_and_day_one(self):
        # (year, 1, 1)
        assert yearly_window(
            start=datetime(2022, 9, 15), end=datetime(2024, 2, 15)
        ) == [
            DateRange(datetime(2022, 9, 15), datetime(2023, 1, 1)),
            DateRange(datetime(2023, 1, 1), datetime(2024, 1, 1)),
            DateRange(datetime(2024, 1, 1), datetime(2024, 2, 15)),
        ]

    def test_when_start_to_end_range_is_less_than_interval_return_start_to_end_daterange(
        self,
    ):
        assert yearly_window(  # yearly, but start to end is less than a year
            start=datetime(2022, 3, 10), end=datetime(2022, 3, 15)
        ) == [DateRange(datetime(2022, 3, 10), datetime(2022, 3, 15))]

    def test_when_enddate_greater_than_interval_return_sequence_and_residual_part(self):
        assert yearly_window(start=datetime(2022, 1, 1), end=datetime(2024, 3, 20)) == [
            DateRange(datetime(2022, 1, 1), datetime(2023, 1, 1)),
            DateRange(datetime(2023, 1, 1), datetime(2024, 1, 1)),
            DateRange(datetime(2024, 1, 1), datetime(2024, 3, 20)),
        ]


class TestGenerateDatesSequence:
    # INPUT
    def test_if_works_with_datetime_input(self):
        assert generate_dates_sequence(
            start=datetime(2025, 3, 5), end=datetime(2025, 3, 7), recurrence=DAILY
        ) == [datetime(2025, 3, 5), datetime(2025, 3, 6), datetime(2025, 3, 7)]

    def test_if_works_with_date_input(self):
        assert generate_dates_sequence(
            start=date(2025, 3, 5), end=date(2025, 3, 7), recurrence=DAILY
        ) == [datetime(2025, 3, 5), datetime(2025, 3, 6), datetime(2025, 3, 7)]

    # END_INCLUDED ARG: general behavior
    def test_when_end_isnt_included_and_start_and_end_are_equal_should_return_only_one(
        self,
    ):
        assert generate_dates_sequence(
            start=datetime(2025, 5, 5), end=datetime(2025, 5, 5), recurrence=DAILY
        ) == [datetime(2025, 5, 5)]
        assert generate_dates_sequence(
            start=datetime(2025, 5, 5), end=datetime(2025, 5, 5), recurrence=WEEKLY
        ) == [datetime(2025, 5, 5)]
        assert generate_dates_sequence(
            start=datetime(2025, 5, 5), end=datetime(2025, 5, 5), recurrence=MONTHLY
        ) == [datetime(2025, 5, 5)]
        assert generate_dates_sequence(
            start=datetime(2025, 5, 5), end=datetime(2025, 5, 5), recurrence=YEARLY
        ) == [datetime(2025, 5, 5)]

    def test_when_end_is_included_and_start_and_end_are_equal_should_return_both(self):
        assert generate_dates_sequence(
            start=datetime(2025, 5, 5),
            end=datetime(2025, 5, 5),
            recurrence=DAILY,
            end_included=True,
        ) == [datetime(2025, 5, 5), datetime(2025, 5, 5)]
        assert generate_dates_sequence(
            start=datetime(2025, 5, 5),
            end=datetime(2025, 5, 5),
            recurrence=WEEKLY,
            end_included=True,
        ) == [datetime(2025, 5, 5), datetime(2025, 5, 5)]
        assert generate_dates_sequence(
            start=datetime(2025, 5, 5),
            end=datetime(2025, 5, 5),
            recurrence=MONTHLY,
            end_included=True,
        ) == [datetime(2025, 5, 5), datetime(2025, 5, 5)]
        assert generate_dates_sequence(
            start=datetime(2025, 5, 5),
            end=datetime(2025, 5, 5),
            recurrence=YEARLY,
            end_included=True,
        ) == [datetime(2025, 5, 5), datetime(2025, 5, 5)]

    # END_INCLUDED ARG: daily behavior
    def test_daily_when_end_isnt_included_should_return_sequence_with_end(self):
        assert generate_dates_sequence(
            start=datetime(2025, 5, 5), end=datetime(2025, 5, 7), recurrence=DAILY
        ) == [datetime(2025, 5, 5), datetime(2025, 5, 6), datetime(2025, 5, 7)]

    def test_daily_when_end_is_included_should_return_sequence_with_end(self):
        assert generate_dates_sequence(
            start=datetime(2025, 5, 5),
            end=datetime(2025, 5, 7),
            recurrence=DAILY,
            end_included=True,
        ) == [datetime(2025, 5, 5), datetime(2025, 5, 6), datetime(2025, 5, 7)]

    # END_INCLUDED ARG: weekly behavior
    def test_weekly_when_end_isnt_included_should_return_sequence_without_end(self):
        assert generate_dates_sequence(
            start=datetime(2025, 5, 5), end=datetime(2025, 5, 15), recurrence=WEEKLY
        ) == [datetime(2025, 5, 5), datetime(2025, 5, 12)]

    def test_weekly_when_end_is_included_should_return_sequence_with_end(self):
        assert generate_dates_sequence(
            start=datetime(2025, 5, 5),
            end=datetime(2025, 5, 15),
            recurrence=WEEKLY,
            end_included=True,
        ) == [datetime(2025, 5, 5), datetime(2025, 5, 12), datetime(2025, 5, 15)]

    # END_INCLUDED ARG: monthly behavior
    def test_monthly_when_end_isnt_included_should_return_sequence_without_end(self):
        assert generate_dates_sequence(
            start=datetime(2025, 5, 5), end=datetime(2025, 6, 15), recurrence=MONTHLY
        ) == [datetime(2025, 5, 5), datetime(2025, 6, 5)]

    def test_monthly_when_end_is_included_should_return_sequence_with_end(self):
        assert generate_dates_sequence(
            start=datetime(2025, 5, 5),
            end=datetime(2025, 6, 15),
            recurrence=MONTHLY,
            end_included=True,
        ) == [datetime(2025, 5, 5), datetime(2025, 6, 5), datetime(2025, 6, 15)]

    # END_INCLUDED ARG: yearly behavior
    def test_yearly_when_end_isnt_included_should_return_sequence_without_end(self):
        assert generate_dates_sequence(
            start=datetime(2025, 5, 5), end=datetime(2026, 7, 15), recurrence=YEARLY
        ) == [datetime(2025, 5, 5), datetime(2026, 5, 5)]

    def test_yearly_when_end_is_included_should_return_sequence_with_end(self):
        assert generate_dates_sequence(
            start=datetime(2025, 5, 5),
            end=datetime(2026, 7, 15),
            recurrence=YEARLY,
            end_included=True,
        ) == [datetime(2025, 5, 5), datetime(2026, 5, 5), datetime(2026, 7, 15)]

    # FORMAT ARG
    def test_if_date_format_is_defined_should_return_date_pattern_strings(self):
        assert generate_dates_sequence(
            start=datetime(2025, 5, 5),
            end=datetime(2025, 5, 7),
            recurrence=DAILY,
            format="%Y-%m-%d",
        ) == ["2025-05-05", "2025-05-06", "2025-05-07"]
        assert generate_dates_sequence(
            start=datetime(2025, 5, 5),
            end=datetime(2025, 5, 7),
            recurrence=DAILY,
            format="%Y/%m/%d",
        ) == ["2025/05/05", "2025/05/06", "2025/05/07"]
        assert generate_dates_sequence(
            start=datetime(2025, 5, 5),
            end=datetime(2025, 5, 7),
            recurrence=DAILY,
            format="%Y%m%d",
        ) == ["20250505", "20250506", "20250507"]
