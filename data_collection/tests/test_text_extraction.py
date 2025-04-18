from datetime import date

from gazette.utils.text_extraction import (
    get_date_from_text,
    get_month_value_from_writing,
)


class TestExtractDateFromText:
    # TEXT ARG
    def test_if_text_should_be_string(self):
        assert get_date_from_text(12.3) is None
        assert get_date_from_text(["1", "2"]) is None
        assert get_date_from_text(False) is None
        assert get_date_from_text(("tu", "pla")) is None
        assert get_date_from_text("") is None

    # SETTINGS: STRICT PARSING = TRUE
    def test_text_missing_information_should_be_parsed(self):
        # no year
        assert get_date_from_text("10 de Março") is None
        assert get_date_from_text("10 de 03") is None
        assert get_date_from_text("10 03") is None
        assert get_date_from_text("1003") is None
        # no month
        assert get_date_from_text("10 2009") is None
        assert get_date_from_text("102009") is None
        # no day
        assert get_date_from_text("Março de 2009") is None
        assert get_date_from_text("03 de 2009") is None
        assert get_date_from_text("03 2009") is None
        assert get_date_from_text("032009") is None

    # CONTENT
    def test_presence_of_ordenation_symbol_should_behave_as_if_without_it(self):
        assert get_date_from_text("15º março 2021") == date(2021, 3, 15)
        assert get_date_from_text("27 10° 1999") == date(1999, 10, 27)
        assert get_date_from_text("01ª 08 1879") == date(1879, 8, 1)

    def test_if_text_with_multiple_whitespaces_is_parsed(self):
        # in separator
        assert get_date_from_text("    01     02      2023       ") == date(2023, 2, 1)
        assert get_date_from_text("    1     2      2023       ") == date(2023, 2, 1)
        # in day
        assert get_date_from_text("2  3 novembro 2028") == date(2028, 11, 23)
        assert get_date_from_text("2  3/novembro/2028") == date(2028, 11, 23)
        # in month
        assert get_date_from_text("3 no  vem  bro 2028") == date(2028, 11, 3)
        assert get_date_from_text("3 1  1 2028") is None
        assert get_date_from_text("3 - 1  1 - 2028") == date(2028, 11, 3)
        # in year
        assert get_date_from_text("3 novembro 2  028") == date(2028, 11, 3)
        assert get_date_from_text("3 novembro 20  28") == date(2028, 11, 3)
        assert get_date_from_text("3 novembro 202  8") == date(2028, 11, 3)

    def test_upper_cased_words_should_be_parsed(self):
        assert get_date_from_text("02 JANEIRO 2023") == date(2023, 1, 2)
        assert get_date_from_text("02 JaNeIrO 2023") == date(2023, 1, 2)
        assert get_date_from_text("02 jAnEiRo 2023") == date(2023, 1, 2)

    def test_word_with_diacritics_should_be_parsed_as_if_without_it(self):
        assert get_date_from_text("4 março 2028") == date(2028, 3, 4)
        assert get_date_from_text("4 marco 2028") == date(2028, 3, 4)
        assert get_date_from_text("4 máíó 2028") == date(2028, 5, 4)
        assert get_date_from_text("4 mâîô 2028") == date(2028, 5, 4)
        assert get_date_from_text("4 mãĩõ 2028") == date(2028, 5, 4)

    def test_month_written_text_should_be_parsed_with_differents_separators(self):
        assert get_date_from_text("23 novembro 2028") == date(2028, 11, 23)
        assert get_date_from_text("23/novembro/2028") == date(2028, 11, 23)
        assert get_date_from_text("23-novembro-2028") == date(2028, 11, 23)
        assert get_date_from_text("23_novembro_2028") == date(2028, 11, 23)
        assert get_date_from_text("23 de novembro de 2028") == date(2028, 11, 23)
        assert get_date_from_text("23denovembrode2028") == date(2028, 11, 23)

    def test_month_written_text_should_be_parsed_without_separator(self):
        assert get_date_from_text("03fevereiro2025") == date(2025, 2, 3)

    def test_full_numbered_text_should_be_parsed_with_differents_separators(self):
        assert get_date_from_text("1 1 1968") == date(1968, 1, 1)
        assert get_date_from_text("1 10 1968") == date(1968, 10, 1)
        assert get_date_from_text("10 1 1968") == date(1968, 1, 10)
        assert get_date_from_text("10 10 1968") == date(1968, 10, 10)
        assert get_date_from_text("10/10/1968") == date(1968, 10, 10)
        assert get_date_from_text("10-10-1968") == date(1968, 10, 10)
        assert get_date_from_text("10_10_1968") == date(1968, 10, 10)
        assert get_date_from_text("10 de 10 de 1968") == date(1968, 10, 10)
        assert get_date_from_text("10de10de1968") == date(1968, 10, 10)

    def test_full_numbered_text_should_be_parsed_without_separator_only_when_eight_digit(
        self,
    ):
        assert get_date_from_text("0010022025") is None  # 001 de 002
        assert get_date_from_text("001022025") is None  # 001 de 02
        assert get_date_from_text("010022025") is None  # 01 de 002
        assert get_date_from_text("01022025") == date(2025, 2, 1)  # 01 de 02
        assert get_date_from_text("1022025") is None  # 1 de 02
        assert get_date_from_text("0122025") is None  # 01 de 2
        assert get_date_from_text("122025") is None  # 1 de 2

    def test_de_separator_shouldnt_conflict_with_dezembro(self):
        assert get_date_from_text("15 de dezembro de 1995") == date(1995, 12, 15)
        assert get_date_from_text("15dedezembrode1995") == date(1995, 12, 15)

    # INCONSISTENCY SCENARIOS
    def test_month_written_text_should_be_parsed_with_only_first_separator(self):
        assert get_date_from_text("03/dezembro2000") == date(2000, 12, 3)
        assert get_date_from_text("03-dezembro2000") == date(2000, 12, 3)
        assert get_date_from_text("03_dezembro2000") == date(2000, 12, 3)
        assert get_date_from_text("03 dezembro2000") == date(2000, 12, 3)
        assert get_date_from_text("03 de dezembro 2000") == date(2000, 12, 3)
        assert get_date_from_text("03 de dezembro2000") == date(2000, 12, 3)
        assert get_date_from_text("03 dedezembro2000") == date(2000, 12, 3)
        assert get_date_from_text("03dedezembro2000") == date(2000, 12, 3)

    def test_month_written_text_should_be_parsed_with_only_second_separator(self):
        assert get_date_from_text("03dezembro/2000") == date(2000, 12, 3)
        assert get_date_from_text("03dezembro-2000") == date(2000, 12, 3)
        assert get_date_from_text("03dezembro_2000") == date(2000, 12, 3)
        assert get_date_from_text("03dezembro 2000") == date(2000, 12, 3)
        assert get_date_from_text("03 dezembro de 2000") == date(2000, 12, 3)
        assert get_date_from_text("03 dezembro de2000") == date(2000, 12, 3)
        assert get_date_from_text("03 dezembrode2000") == date(2000, 12, 3)
        assert get_date_from_text("03dezembrode2000") == date(2000, 12, 3)

    def test_full_numbered_text_should_be_parsed_with_only_first_separator_when_eight_digit(
        self,
    ):
        assert get_date_from_text("01 012025") == date(2025, 1, 1)
        assert get_date_from_text("01 12025") is None
        assert get_date_from_text("1 012025") is None
        assert get_date_from_text("1 12025") is None

    def test_full_numbered_text_should_be_parsed_with_only_second_separator_when_eight_digit(
        self,
    ):
        assert get_date_from_text("0101 2025") == date(2025, 1, 1)
        assert get_date_from_text("011 2025") is None
        assert get_date_from_text("101 2025") is None
        assert get_date_from_text("11 2025") is None

    def test_if_recognizes_date_from_month_with_typo(self):
        assert get_date_from_text("8 de janiro de 2030") == date(2030, 1, 8)
        assert get_date_from_text("8 de feverero de 2030") == date(2030, 2, 8)
        assert get_date_from_text("8 de maro de 2030") == date(2030, 3, 8)
        assert get_date_from_text("8 de abriu de 2030") == date(2030, 4, 8)
        assert get_date_from_text("8 de maiio de 2030") == date(2030, 5, 8)
        assert get_date_from_text("8 de juno de 2030") == date(2030, 6, 8)
        assert get_date_from_text("8 de julo de 2030") == date(2030, 7, 8)
        assert get_date_from_text("8 de agosti de 2030") == date(2030, 8, 8)
        assert get_date_from_text("8 de setembu de 2030") == date(2030, 9, 8)
        assert get_date_from_text("8 de oubro de 2030") == date(2030, 10, 8)
        assert get_date_from_text("8 de novem de 2030") == date(2030, 11, 8)
        assert get_date_from_text("8 de zembro de 2030") == date(2030, 12, 8)

    def test_text_with_inexistent_date_should_return_none(self):
        assert get_date_from_text("31 02 2025") is None
        assert get_date_from_text("31 fevereiro 2025") is None
        assert get_date_from_text("31 feveriro 2025") is None

    def test_if_date_is_captured_when_around_more_text(self):  # real cases from sites
        assert get_date_from_text("Publicado dia 28 de março 2025") == date(2025, 3, 28)
        assert get_date_from_text("Terça-feira, 9 de julho de 2024") == date(2024, 7, 9)
        assert get_date_from_text("18/1/2024 - Edição Extra") == date(2024, 1, 18)
        assert get_date_from_text(
            "26 de dezembro de 2005 Encarte da Lei 9.881 parte 1"
        ) == date(2005, 12, 26)
        assert get_date_from_text("edicao extra 27 de dezembro de 2005") == date(
            2005, 12, 27
        )
        assert get_date_from_text("1ª edição extra de 30 de dezembro de 2005") == date(
            2005, 12, 30
        )
        assert get_date_from_text("1º de junho de 2005") == date(2005, 6, 1)
        assert get_date_from_text("6 de junho de 2005 - suplemento") == date(2005, 6, 6)
        assert get_date_from_text("29 de dezembro de 2006 - pags 41 a 60") == date(
            2006, 12, 29
        )
        assert get_date_from_text(
            "2ª Edição de 29 de dezembro de 2006 - pág 52 e 53"
        ) == date(2006, 12, 29)


class TestGetMonthValueFromWriting:
    def test_if_whitespace_in_extremities_is_ignored(self):
        assert get_month_value_from_writing("   janero    ") == "01"

    def test_if_upper_case_makes_is_ignored(self):
        assert get_month_value_from_writing("JunHo") == "06"
        assert get_month_value_from_writing("jUlhO") == "07"
        assert get_month_value_from_writing("AGOSTO") == "08"

    def test_if_common_abbreviation_is_recognized_correctly(self):
        assert get_month_value_from_writing("jan") == "01"
        assert get_month_value_from_writing("fev") == "02"
        assert get_month_value_from_writing("mar") == "03"
        assert get_month_value_from_writing("abr") == "04"
        assert get_month_value_from_writing("mai") == "05"
        assert get_month_value_from_writing("jun") == "06"
        assert get_month_value_from_writing("jul") == "07"
        assert get_month_value_from_writing("ago") == "08"
        assert get_month_value_from_writing("set") == "09"
        assert get_month_value_from_writing("out") == "10"
        assert get_month_value_from_writing("nov") == "11"
        assert get_month_value_from_writing("dez") == "12"

    def test_janeiro_recognition(self):
        # 1 letter is missing
        assert get_month_value_from_writing("aneiro") == "01"
        assert get_month_value_from_writing("jneiro") == "01"
        assert get_month_value_from_writing("jaeiro") == "01"
        assert get_month_value_from_writing("janiro") == "01"
        assert get_month_value_from_writing("janero") == "01"
        assert get_month_value_from_writing("janeio") == "01"

        # progressive missing letters
        assert get_month_value_from_writing("janeir") == "01"
        assert get_month_value_from_writing("janei") == "01"
        assert get_month_value_from_writing("jane") == "01"
        assert get_month_value_from_writing("jan") == "01"
        assert get_month_value_from_writing("ja") == "01"

        # letters position changed
        assert get_month_value_from_writing("janiero") == "01"
        assert get_month_value_from_writing("janeior") == "01"
        assert get_month_value_from_writing("jnaeiro") == "01"

    def test_junho_recognition(self):
        # 1 letter is missing
        assert get_month_value_from_writing("unho") == "06"
        assert get_month_value_from_writing("jnho") == "06"
        # assert get_month_value_from_writing("juho") == "06"  # poderia ser julho
        assert get_month_value_from_writing("juno") == "06"
        assert get_month_value_from_writing("junh") == "06"

        # progressive missing letters
        assert get_month_value_from_writing("junh") == "06"
        assert get_month_value_from_writing("jun") == "06"
        # assert get_month_value_from_writing("ju") == "06"     # poderia ser julho

        # letters position changed
        assert get_month_value_from_writing("juhno") == "06"
        assert get_month_value_from_writing("jnuho") == "06"
        assert get_month_value_from_writing("junoh") == "06"
        assert get_month_value_from_writing("jonhu") == "06"

    def test_julho_recognition(self):
        # 1 letter is missing
        assert get_month_value_from_writing("ulho") == "07"
        assert get_month_value_from_writing("jlho") == "07"
        # assert get_month_value_from_writing("juho") == "07"    # poderia ser junho
        assert get_month_value_from_writing("julo") == "07"
        assert get_month_value_from_writing("julh") == "07"

        # progressive missing letters
        assert get_month_value_from_writing("julh") == "07"
        assert get_month_value_from_writing("jul") == "07"
        # assert get_month_value_from_writing("ju") == "07"       # poderia ser junho

        # letters position changed
        # assert get_month_value_from_writing("juhlo") == "07"   # sendo reconhecido como junho
        # assert get_month_value_from_writing("jluho") == "07"     # sendo reconhecido como junho
        assert get_month_value_from_writing("juloh") == "07"
        assert get_month_value_from_writing("jolhu") == "07"
