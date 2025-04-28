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

    So, this works with known dateparser cases in pt-br, with commonly used separators
    as '-', '/', 'de', etc. And adds ways to deal with inconsistent situations,
    such as when there's only one separator, ordenation symbol (ªº) present
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
    if not isinstance(text, str) or len(text) == 0:
        return None

    settings = {"DATE_ORDER": "DMY", "STRICT_PARSING": True}

    # normalize text
    text = unidecode(re.sub("[°ºª]", "", text)).lower().strip()

    # Try to apply dateparser as always ...
    parsed_date = parse(text, languages=["pt"], settings=settings)
    if parsed_date:
        return parsed_date.date()

    # ... it didnt work, so try to parse manually

    # note: in general, day and year are numbers, only month vary between being
    # written or numbered. At the same time, a full numbered date text depend more
    # of separator presence and number length logic to date be identified. But when
    # month is written, month text already works as separator between numbers

    if re.sub("[ -/_de]+", "", text).isdigit():
        return get_date_from_numbered_text(text)
    return get_date_from_month_written_text(text)


def get_date_from_numbered_text(text, separator=r"[ /_-]"):
    """Returns date identified in a numbered text

    Date is identified through four cases, related to separator presence:
    (a) 2 separatos: separates all parts
    format: (D/DD) (M/MM) (YYYY)
    examples: 1 1 1111 | 1 11 1111 | 11 1 1111 | 11 11 1111
    possible to parse in any day, month, year length since its properly separated

    (b) 1 separator, the first one: separates day from month+year part
    format: (D/DD) (M/MM)(YYYY)
    examples: 1 11111 | 1 111111 | 11 11111 | 11 111111
    possible to parse if we assume year with 4 char length

    (c) 1 separator, the second one: separates year from day+month part
    format: (DD)(MM) (YYYY)
    example: 1111 1111
    possible to parse only when day and month have 2 char length

    (d) no separator:
    format: (DD)(MM)(YYYY)
    example: 11111111
    possible to parse only if 2 char day, 2 char month and 4 char year
    """
    if not isinstance(text, str) or len(text) == 0:
        return None

    regex_list = [
        rf"(\d+){separator}(\d+){separator}(\d+)",  # case (a)
        rf"(\d+){separator}(\d{{1,2}})(\d{{4}})",  # case (b)
        rf"(\d{{2}})(\d{{2}}){separator}(\d+)",  # case (c)
        r"(\d{2})(\d{2})(\d{4})",  # case (d)
    ]

    text = re.sub(" +", " ", text.replace("de", ""))
    for regex_case in regex_list:
        date = _apply_regex(regex_case, text, 1, 2, 3)
        if date:
            return date
    return None


def get_date_from_month_written_text(text, separator=r"[/_-]"):
    """Returns date identified in text where month name is written in full

    To avoid dirty strings, this func works by concatenating all text to apply
    regex as parsing strategy. Also, replaces 'de' occurences to make 'de' separated
    cases behave as if hyphen separated avoiding conflict with 'de' of 'dezembro'
    """
    if not isinstance(text, str) or len(text) == 0:
        return None

    concatenated_text = re.sub(" ", "", text)
    text = concatenated_text.replace("de", "-").replace("-z", "dez")

    # (D or DD)separators(month)separators(YYYY)
    regex = rf"(\d{{1,2}}){separator}?([a-z0-9]+){separator}?(\d{{4}})"
    return _apply_regex(regex, text, 1, 2, 3)


def get_month_value(month_text):
    """Identify month number from a text

    Uses Levenshtein Distance algorithm from thefuzz lib to recognize text proximity
    as strategy to fix mistyped month

    Args:
        month_text (str): text written or numbered about a month

    Returns:
        An int of month value, if match. Otherwise, returns None.
    """
    if not isinstance(month_text, str) or len(month_text) == 0:
        return None

    MONTHS = {
        "janeiro": 1,
        "fevereiro": 2,
        "marco": 3,
        "abril": 4,
        "maio": 5,
        "junho": 6,
        "julho": 7,
        "agosto": 8,
        "setembro": 9,
        "outubro": 10,
        "novembro": 11,
        "dezembro": 12,
    }

    conflicting_cases = ["juho"]

    month_text = unidecode(month_text.strip().lower())

    if month_text.isdigit() and int(month_text) in MONTHS.values():
        return int(month_text)

    if len(month_text) < 3 or month_text in conflicting_cases:
        return None

    if month_text not in MONTHS:
        result = process.extractOne(month_text, MONTHS.keys(), score_cutoff=80)
        return MONTHS[result[0]] if result else None

    return MONTHS[month_text]


def _apply_regex(regex, text, day_index, month_index, year_index):
    """Returns date by applying regex to text, in day, month and year order, fixing
    month writing in pt-br if necessary

    Note:
        By now, only DMY order is used when evoking this func, but the intention
        is to allow more orders in future, on demand.

    Examples:
        >>> _apply_regex("...", "10 maio 2000", 1, 2, 3)       # DMY order
        date(2000, 5, 10)
        >>> _apply_regex("...", "2000-05-10", 3, 2, 1)         # YMD order
        date(2000, 5, 10)
        >>> _apply_regex("...", "May 10 2000", 2, 1, 3)        # MDY order
        date(2000, 5, 10)

    Args:
        regex (str): a string representing a regex pattern
        text (str): text to apply regex to
        day_index (int): group index where day value is expected
        month_index (int): group index where month is expected
        year_index (int): group index where year is expected

    Returns:
        date: object representing date regex-founded in text
        None: if regex didn't match or date doesn't exist
    """
    match = re.search(regex, text)

    if match:
        day = match.group(day_index)
        month = get_month_value(match.group(month_index))
        year = match.group(year_index)

        try:
            parsed_date = date(int(year), month, int(day))
            return parsed_date
        except Exception:
            return None
    return None
