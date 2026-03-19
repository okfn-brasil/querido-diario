from datetime import date

import pytest

from gazette.utils.nucleogov import (
    Diario,
    DiarioMidia,
    DiarioPage,
    DiarioTipo,
    is_extra_edition,
    parse_date,
)


class TestParseDate:
    def test_valid_date(self):
        assert parse_date("2026-03-19") == date(2026, 3, 19)

    def test_valid_date_single_digit_month_day(self):
        assert parse_date("2021-1-5") == date(2021, 1, 5)

    def test_invalid_format_raises(self):
        with pytest.raises(ValueError):
            parse_date("19/03/2026")

    def test_empty_string_raises(self):
        with pytest.raises(ValueError):
            parse_date("")


class TestIsExtraEdition:
    def test_diario_oficial_is_not_extra(self):
        assert is_extra_edition("Diário Oficial") is False

    def test_edicao_semanal_is_not_extra(self):
        assert is_extra_edition("Edição Semanal") is False

    def test_edicao_especial_is_extra(self):
        assert is_extra_edition("Edição Especial") is True

    def test_edicao_suplementar_is_extra(self):
        assert is_extra_edition("Edição Suplementar") is True

    def test_edicao_extraordinaria_is_extra(self):
        assert is_extra_edition("Edição Extraordinária") is True

    def test_case_insensitive(self):
        assert is_extra_edition("DIÁRIO OFICIAL") is False
        assert is_extra_edition("EDIÇÃO ESPECIAL") is True

    def test_empty_string_is_extra(self):
        assert is_extra_edition("") is True


class TestDiarioTipo:
    def test_from_dict(self):
        tipo = DiarioTipo.from_dict({"id": 1, "descricao": "Diário Oficial"})
        assert tipo.descricao == "Diário Oficial"

    def test_missing_descricao_raises(self):
        with pytest.raises(KeyError):
            DiarioTipo.from_dict({"id": 1})


class TestDiarioMidia:
    def test_from_dict(self):
        midia = DiarioMidia.from_dict({"url": "https://example.com/file.pdf"})
        assert midia.url == "https://example.com/file.pdf"

    def test_missing_url_raises(self):
        with pytest.raises(KeyError):
            DiarioMidia.from_dict({"name": "file.pdf"})


class TestDiario:
    VALID_DIARIO = {
        "data": "2026-03-19",
        "numero": "052",
        "tipo": {"id": 1, "descricao": "Diário Oficial"},
        "midias": [{"url": "https://example.com/file.pdf"}],
    }

    EXTRA_DIARIO = {
        "data": "2026-03-19",
        "numero": "012",
        "tipo": {"id": 2, "descricao": "Edição Especial"},
        "midias": [{"url": "https://example.com/extra.pdf"}],
    }

    def test_from_dict(self):
        diario = Diario.from_dict(self.VALID_DIARIO)
        assert diario.data == date(2026, 3, 19)
        assert diario.numero == "052"
        assert diario.tipo.descricao == "Diário Oficial"

    def test_file_urls(self):
        diario = Diario.from_dict(self.VALID_DIARIO)
        assert diario.file_urls == ["https://example.com/file.pdf"]

    def test_is_extra_edition_false(self):
        diario = Diario.from_dict(self.VALID_DIARIO)
        assert diario.is_extra_edition is False

    def test_is_extra_edition_true(self):
        diario = Diario.from_dict(self.EXTRA_DIARIO)
        assert diario.is_extra_edition is True

    def test_missing_midias_defaults_to_empty(self):
        data = {**self.VALID_DIARIO}
        del data["midias"]
        diario = Diario.from_dict(data)
        assert diario.file_urls == []

    def test_missing_numero_defaults_to_empty(self):
        data = {**self.VALID_DIARIO}
        del data["numero"]
        diario = Diario.from_dict(data)
        assert diario.numero == ""

    def test_missing_data_raises(self):
        with pytest.raises(KeyError):
            Diario.from_dict({"numero": "1", "tipo": {"descricao": "X"}, "midias": []})

    def test_missing_tipo_raises(self):
        with pytest.raises(KeyError):
            Diario.from_dict({"data": "2026-01-01", "midias": []})


class TestDiarioPage:
    def test_has_next_page_true(self):
        page = DiarioPage(current_page=1, last_page=5, diarios=[])
        assert page.has_next_page is True
        assert page.next_page == 2

    def test_has_next_page_false(self):
        page = DiarioPage(current_page=5, last_page=5, diarios=[])
        assert page.has_next_page is False


class TestApiContractBreaks:
    """Tests that API structure changes produce clear, diagnosable errors."""

    VALID_DIARIO = {
        "data": "2026-03-19",
        "numero": "052",
        "tipo": {"id": 1, "descricao": "Diário Oficial"},
        "midias": [{"url": "https://example.com/file.pdf"}],
    }

    def test_data_field_renamed(self):
        broken = {**self.VALID_DIARIO, "data": None}
        del broken["data"]
        broken["date"] = "2026-03-19"
        with pytest.raises(KeyError, match="data"):
            Diario.from_dict(broken)

    def test_tipo_field_renamed(self):
        broken = {**self.VALID_DIARIO}
        del broken["tipo"]
        broken["type"] = {"id": 1, "descricao": "Diário Oficial"}
        with pytest.raises(KeyError, match="tipo"):
            Diario.from_dict(broken)

    def test_tipo_descricao_renamed(self):
        broken = {
            **self.VALID_DIARIO,
            "tipo": {"id": 1, "description": "Diário Oficial"},
        }
        with pytest.raises(KeyError, match="descricao"):
            Diario.from_dict(broken)

    def test_midias_url_renamed(self):
        broken = {
            **self.VALID_DIARIO,
            "midias": [{"link": "https://example.com/file.pdf"}],
        }
        with pytest.raises(KeyError, match="url"):
            Diario.from_dict(broken)

    def test_data_format_changed(self):
        broken = {**self.VALID_DIARIO, "data": "19/03/2026"}
        with pytest.raises(ValueError):
            Diario.from_dict(broken)

    def test_pagination_field_missing(self):
        payload = {"data": [], "current_page": 1}
        with pytest.raises(KeyError, match="last_page"):
            DiarioPage(
                current_page=payload["current_page"],
                last_page=payload["last_page"],
                diarios=[],
            )
