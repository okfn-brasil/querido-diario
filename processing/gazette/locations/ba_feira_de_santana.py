import re
import string
import datetime

from .base_parser import BaseParser


class BaFeiraDeSantana(BaseParser):
    BIDDING_EXEMPTIONS_MARKER = "Dispensa de Licitação"
    DATE_REGEXP = r"([0-9]{2}/?[0-9]{2}/?2[0-9]{3})"

    def bidding_exemptions(self):
        exemptions = [
            self._parse_bidding_exemption(exemption)
            for exemption in self._bidding_exemption_sections()
        ]

        return exemptions

    def _bidding_exemption_sections(self):
        sections = self.text.split(self.BIDDING_EXEMPTIONS_MARKER)[1:]

        return [section.split("\n\n")[0] for section in sections]

    def _parse_bidding_exemption(self, exemption_str):
        _remove_newlines_and_multiple_whitespaces = lambda text: re.sub(
            r"\s+", " ", text
        )
        exemption_str = _remove_newlines_and_multiple_whitespaces(exemption_str)

        field_to_token = {
            "CONTRATANTE": "CONTRATANTE",
            "OBJETO": "OBJETO",
            "CONTRATADA": "CONTRATADA",
            "FONTE": "FONTE",
            "PROJETO/ATIVIDADE": "PROJETO/ATIVIDADE",
            "SUBELEMENTO DE DESPESA": r"Sub\. elemento de despesa",
            "UNIDADE ORCAMENTARIA": "Unidade Orçamentária",
        }

        exemption = {
            key: self._extract_value(exemption_str, gazette_token)
            for key, gazette_token in field_to_token.items()
        }

        exemption.update(
            {
                "NUMERO": _extract_regexp(
                    exemption_str, r"Nº:?\s*([0-9]+-[0-9]{4}-[0-9]+-?[A-Z])"
                ),
                "CONTRATANTE": self._extract_value(exemption_str, "contratante"),
                "VALOR": self._parse_currency(exemption_str),
                "DATA": self._parse_date(exemption_str),
            }
        )

        # TODO(2018-12-01): Validate that mandatory keys exist (e.g. "NUMERO")

        return exemption

    def _extract_value(self, exemption_str, token):
        tokens = [
            "objeto",
            "contratante",
            "contratada",
            "valor",
            "data",
            "Nº",
            "fonte",
            "PROJETO/ATIVIDADE",
            r"Sub\. elemento de despesa",
            "Unidade Orçamentária",
            "$",  # Handle case where we"re extracting the last value.
        ]

        tokens_group = f"({'|'.join(tokens)})"

        regexp = f"{token}[:.-]?\s*(.+?){tokens_group}"

        return _extract_regexp(exemption_str, regexp)

    def _parse_currency(self, exemption_str):
        value = _extract_regexp(exemption_str, r"R\$\s*([0-9.]+,[0-9]{2})")

        if value:
            value = value.replace(".", "").replace(",", ".")
            value = float(value)

        return value

    def _parse_date(self, exemption_str):
        date = _extract_regexp(exemption_str, self.DATE_REGEXP)

        if date:
            date = date.replace("/", "")
            date = datetime.datetime.strptime(date, "%d%m%Y").date()

        return date


def _extract_regexp(text, regexp):
    groups = re.search(regexp, text, re.IGNORECASE)

    if groups:
        return groups.group(1).strip(string.whitespace + string.punctuation + "–")
