import re
from datetime import date

from dateparser import parse
from text_unidecode import unidecode
from thefuzz import process


def get_date_from_text(text):
    """Return date identified in text

    This func exists to extend date recognition cases that dateparser lib doesn't
    cover. The basic logic is: first try to get date using dateparser, if it
    doesn't work, try to get it using regex.

    So, this works with known dateparser cases (formats like: strictly numbered
    string, month in full writing in pt-br, commonly used separators as '-', '/',
    'de', ' ' or without it). Adds ways to deal with inconsistent situations,
    such as when there's only one separator in text, ordenation symbol (ªº) present
    or mistyped month. Check test_dates.py in tests/ directory to see examples.

    By default, it's set to do stric_parsing, meaning it doesn't try to parse
    incomplete data, and only handles date in day month year order (DMY) for now,
    because its enough for all using cases (but an improvement can be implemented
    in the future, on demand)

    Args:
        text: string with date text in it
    Returns:
        Date object, if able to parse. Otherwise, returns None.
    """
    if not isinstance(text, str):
        return None

    order = "DMY"
    settings = {"DATE_ORDER": order, "STRICT_PARSING": True}

    # normalize input
    text = re.sub("[°ºª]", "", text)
    normalized_text = unidecode(re.sub(" +", " ", text).strip().lower())

    # To avoid issues with dirty strings, this function uses full concatenated text preferably
    # 1nov2025 > month behaves as separator, allowing numbers identification
    # 1112025 > numbered str might has ambiguity (it is 1/11 or 11/1 or 11/12/025?)
    concatenated_text = re.sub(" ", "", normalized_text)

    # HANDLES FULL NUMBERED LIMITATIONS...
    is_full_numbered = concatenated_text.isdigit()
    has_space_separators = sum(char == " " for char in normalized_text) == 2
    if is_full_numbered:
        # 1- space is a separator. Concatenation will ruin its parse
        if has_space_separators:  # D M YYYY | D MM YYYY | DD M YYYY | DD MM YYYY
            parsed_date = parse(normalized_text, languages=["pt"], settings=settings)
            if parsed_date:
                return parsed_date.date()
        # 2- there is no separator. Only possible to parse when it has 8 digits
        if len(concatenated_text) != 8:  # exactly DDMMYYYY
            return None

    # ... FOLLOWS DEFAULT FLOW (with full concatenated string)

    # replace 'de' separator, without conflict with 'de' of 'dezembro'
    # note: makes 'de' cases behave as if DD - MM - AAAA
    text = concatenated_text.replace("de", "-").replace("-z", "dez")

    # TRY TO APPLY DATEPARSER PARSING
    parsed_date = parse(text, languages=["pt"], settings=settings)
    if parsed_date:
        return parsed_date.date()

    # TRY TO APPLY REGEX PARSING

    # create order sensibility.
    regex_date_order = ["", "", ""]

    day_index = order.index("D")
    month_index = order.index("M")
    year_index = order.index("Y")

    regex_date_order[day_index] = r"(\d{1,2})"
    regex_date_order[month_index] = r"(\d{1,2}|[a-z]+)"
    regex_date_order[year_index] = r"(\d{4})"

    # builds a complete search regex, like
    # (D or M or Y) separators (D or M or Y) separators (D or M or Y)
    regex = r"\s?[/_-]?\s?".join(regex_date_order)
    raw_date = re.search(regex, text)

    if raw_date:
        # groups matched in same order as regex_date_order
        day = raw_date.group(day_index + 1)
        month = raw_date.group(month_index + 1)
        year = raw_date.group(year_index + 1)

        if month.isalpha():
            # verify if month is mistyped
            month = get_month_value_from_writing(month)

        try:
            parsed_date = date(int(year), int(month), int(day))
        except Exception:
            return None

        return parsed_date

    return None


def get_month_value_from_writing(month_text):
    """Identify month number from a text with typing errors in month.

    Uses Levenshtein Distance algorithm from thefuzz lib to recognize text proximity

    Args:
        month_text: str of month written in full
    Returns:
        A string with month number, if match. Otherwise, returns None.
    """
    MONTHS = {
        "janeiro": "01",
        "fevereiro": "02",
        "marco": "03",
        "abril": "04",
        "maio": "05",
        "junho": "06",
        "julho": "07",
        "agosto": "08",
        "setembro": "09",
        "outubro": "10",
        "novembro": "11",
        "dezembro": "12",
    }

    month_text = unidecode(month_text.strip().lower())
    if month_text not in MONTHS:
        matched_info = process.extractOne(month_text, MONTHS.keys())
        return MONTHS[matched_info[0]]
    return MONTHS[month_text]
