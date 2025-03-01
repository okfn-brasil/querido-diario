import re

import dateparser
from fuzzywuzzy import process

MONTHS = [
    "janeiro",
    "fevereiro",
    "março",
    "abril",
    "maio",
    "junho",
    "julho",
    "agosto",
    "setembro",
    "outubro",
    "novembro",
    "dezembro",
]


def date_from_text_with_fuzzy_match(text):
    """Extract a date from a text. This method attempts to correct typing errors in the month.

    Args:
        text: A text containing a date with the name of the month full version (%B)
    Returns:
        The date, if match. Otherwise, returns None.
    """

    text = re.sub(" +", " ", text).strip()
    match_date = re.search(r"\d{1,2}º?(\sde)? +(\w+)(\sde)? +\d{4}", text)
    if not match_date:
        return None

    raw_date = match_date.group(0)
    raw_date = raw_date.replace("º", "").replace("°", "")
    month = match_date.group(2)
    if month.lower() not in MONTHS:
        match_month, score = process.extractOne(month, MONTHS)
        if score < 70:
            return None
        raw_date = raw_date.replace(month, match_month)

    parsed_datetime = dateparser.parse(raw_date, languages=["pt"])
    return parsed_datetime.date() if parsed_datetime else None
