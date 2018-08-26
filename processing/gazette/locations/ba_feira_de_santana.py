import re
import datetime

from .base_parser import BaseParser


class BaFeiraDeSantana(BaseParser):
    BIDDING_EXEMPTIONS_MARKER = "Dispensa de Licitação"
    DATE_REGEXP = r"([0-9]{2}/?[0-9]{2}/?[0-9]{4})"

    def bidding_exemptions(self):
        exemptions = [
            self._parse_bidding_exemption(exemption)
            for exemption in self._bidding_exemption_sections()
        ]

        return exemptions

    def _bidding_exemption_sections(self):
        sections = self.text.split(self.BIDDING_EXEMPTIONS_MARKER)[1:]

        if sections:
            last_section = sections[-1]
            date_match = re.search(self.DATE_REGEXP, last_section)
            if date_match:
                sections[-1] = last_section[: date_match.end()]

        return sections

    def _parse_bidding_exemption(self, exemption_str):
        exemption = {
            "NUMERO": _extract_regexp(exemption_str, r"Nº:\s*(.+)CONTRATANTE"),
            "CONTRATANTE": _extract_regexp(
                exemption_str, r"CONTRATANTE:\s*(.+),.*OBJETO", re.DOTALL
            ),
            "OBJETO": _extract_regexp(
                exemption_str, r"OBJETO:\s*(.+)CONTRATADA", re.DOTALL
            ),
            "CONTRATADA": _extract_regexp(
                exemption_str, r"CONTRATADA:\s*(.+)VALOR", re.DOTALL
            ),
            "VALOR": self._parse_value(exemption_str),
            "DATA": self._parse_date(exemption_str),
        }

        return exemption

    def _parse_value(self, exemption_str):
        value = _extract_regexp(exemption_str, r"R\$\s*([0-9.]+,[0-9]{2})")
        if value:
            value = value.replace(".", "").replace(",", ".")
            value = float(value)

        return value

    def _parse_date(self, exemption_str):
        date = _extract_regexp(exemption_str, "{}[.\s]*$".format(self.DATE_REGEXP))
        if date:
            date = date.replace("/", "")
            date = datetime.datetime.strptime(date, "%d%m%Y")
            date = date.date()

        return date


def _extract_regexp(text, regexp, options=0):
    groups = re.search(regexp, text, options)

    if groups:
        value = groups.group(1).strip()
        return value.replace("\n", " ")
