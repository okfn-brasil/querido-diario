from datetime import date

from gazette.utils.extraction import (
    get_date_from_month_written_text,
    get_date_from_numbered_text,
    get_date_from_text,
    get_month_value,
)


class TestExtractDateFromText:
    # TEXT ARG
    def test_if_text_should_be_string(self):
        assert get_date_from_text(None) is None
        assert get_date_from_text("") is None
        assert get_date_from_text([]) is None

    def test_if_text_is_empty_string_should_return_none(self):
        assert get_date_from_text("") is None

    # CONTENT
    def test_presence_of_ordenation_symbol_should_behave_as_if_without_it(self):
        assert get_date_from_text("15º março 2021") == date(2021, 3, 15)
        assert get_date_from_text("27 10° 1999") == date(1999, 10, 27)
        assert get_date_from_text("01ª 08 1879") == date(1879, 8, 1)

    def test_if_text_with_multiple_whitespaces_is_parsed(self):
        # space in separator
        assert get_date_from_text("01       02        2023") == date(2023, 2, 1)
        assert get_date_from_text("01    fevereiro    2023") == date(2023, 2, 1)

    def test_upper_cased_words_should_be_parsed(self):
        assert get_date_from_text("02 JaNeIrO 2023") == date(2023, 1, 2)
        assert get_date_from_text("02 jAnEiRo 2023") == date(2023, 1, 2)

    def test_if_text_with_diacritics_should_be_parsed_as_if_without_it(self):
        assert get_date_from_text("4 março 2028") == date(2028, 3, 4)
        assert get_date_from_text("4 máíó 2028") == date(2028, 5, 4)
        assert get_date_from_text("4 mâîô 2028") == date(2028, 5, 4)
        assert get_date_from_text("4 mãĩõ 2028") == date(2028, 5, 4)

    def test_if_two_digit_year_is_parsed(self):
        # parses as if 19 century
        assert get_date_from_text("1 1 70") == date(1970, 1, 1)
        assert get_date_from_text("1 1 80") == date(1980, 1, 1)
        assert get_date_from_text("1 1 90") == date(1990, 1, 1)
        # parses as if 20 century
        assert get_date_from_text("1 1 00") == date(2000, 1, 1)
        assert get_date_from_text("1 1 10") == date(2010, 1, 1)
        assert get_date_from_text("1 1 20") == date(2020, 1, 1)
        assert get_date_from_text("1 1 30") == date(2030, 1, 1)
        assert get_date_from_text("1 1 40") == date(2040, 1, 1)
        assert get_date_from_text("1 1 50") == date(2050, 1, 1)
        assert get_date_from_text("1 1 60") == date(2060, 1, 1)

    # INCONSISTENCY
    # STRICT_PARSING = TRUE
    def test_if_text_with_missing_information_shouldnt_be_parsed(self):
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

    # REAL CASES FROM SITES
    def test_if_text_contains_a_interval_return_first_complete_date_possible(self):
        assert get_date_from_text("03/06/2022 a 09/06/2022") == date(2022, 6, 3)
        assert get_date_from_text("de 27/05/2022 à 02/06/2022") == date(2022, 5, 27)
        assert get_date_from_text("17 a 23 de outubro de 2008") == date(2008, 10, 23)
        assert get_date_from_text("de 13/06/2007 à 19/06/2007") == date(2007, 6, 13)
        assert get_date_from_text("de 27 de julho a 02 de agosto de 2007") == date(
            2007, 8, 2
        )

    def test_if_date_is_captured_when_around_more_text(self):
        assert get_date_from_text("Publicado dia 28 de março 2025") == date(2025, 3, 28)
        assert get_date_from_text("Terça-feira, 9 de julho de 2024") == date(2024, 7, 9)
        assert get_date_from_text(
            "26 de dezembro de 2005 Encarte da Lei 9.881 parte 1"
        ) == date(2005, 12, 26)
        assert get_date_from_text("1ª edição extra de 30 de dezembro de 2005") == date(
            2005, 12, 30
        )
        assert get_date_from_text(
            "2ª Edição de 29 de dezembro de 2006 - pág 52 e 53"
        ) == date(2006, 12, 29)
        assert get_date_from_text("04 de Abril0 de 2024") == date(2024, 4, 4)
        assert get_date_from_text("04 Abril0 2024") == date(2024, 4, 4)
        assert get_date_from_text("04Abril02024") == date(2024, 4, 4)


class TestGetDateFromNumberedText:
    # INPUT / ARG
    def test_if_text_isnt_string_should_return_none(self):
        assert get_date_from_numbered_text(None) is None
        assert get_date_from_numbered_text(1.2) is None
        assert get_date_from_numbered_text([]) is None
        assert get_date_from_numbered_text((1, 2)) is None

    def test_if_text_is_empty_string_should_return_none(self):
        assert get_date_from_numbered_text("") is None

    def test_if_text_has_alphabetic_char_should_return_none(self):
        assert get_date_from_numbered_text("30 de novembro de1917") is None

    # CONTENT
    # 2 separators
    def test_date_should_be_recognized_when_two_separators_presence(self):
        # whitespace
        assert get_date_from_numbered_text("1 1 1968") == date(1968, 1, 1)
        assert get_date_from_numbered_text("1 10 1968") == date(1968, 10, 1)
        assert get_date_from_numbered_text("10 1 1968") == date(1968, 1, 10)
        assert get_date_from_numbered_text("10 10 1968") == date(1968, 10, 10)
        # slash
        assert get_date_from_numbered_text("1/1/1968") == date(1968, 1, 1)
        assert get_date_from_numbered_text("1/10/1968") == date(1968, 10, 1)
        assert get_date_from_numbered_text("10/1/1968") == date(1968, 1, 10)
        assert get_date_from_numbered_text("10/10/1968") == date(1968, 10, 10)
        # hyphen
        assert get_date_from_numbered_text("1-1-1968") == date(1968, 1, 1)
        assert get_date_from_numbered_text("1-10-1968") == date(1968, 10, 1)
        assert get_date_from_numbered_text("10-1-1968") == date(1968, 1, 10)
        assert get_date_from_numbered_text("10-10-1968") == date(1968, 10, 10)
        # underscore
        assert get_date_from_numbered_text("1_1_1968") == date(1968, 1, 1)
        assert get_date_from_numbered_text("1_10_1968") == date(1968, 10, 1)
        assert get_date_from_numbered_text("10_1_1968") == date(1968, 1, 10)
        assert get_date_from_numbered_text("10_10_1968") == date(1968, 10, 10)
        # de
        assert get_date_from_numbered_text("1 de 1 de 1968") == date(1968, 1, 1)
        assert get_date_from_numbered_text("1 de 10 de 1968") == date(1968, 10, 1)
        assert get_date_from_numbered_text("10 de 1 de 1968") == date(1968, 1, 10)
        assert get_date_from_numbered_text("10 de 10 de 1968") == date(1968, 10, 10)

    # only first separator
    def test_date_should_be_recognized_with_only_first_separator(self):
        # whitespace
        assert get_date_from_numbered_text("1 11968") == date(1968, 1, 1)
        assert get_date_from_numbered_text("1 101968") == date(1968, 10, 1)
        assert get_date_from_numbered_text("10 11968") == date(1968, 1, 10)
        assert get_date_from_numbered_text("10 101968") == date(1968, 10, 10)
        # slash
        assert get_date_from_numbered_text("1/11968") == date(1968, 1, 1)
        assert get_date_from_numbered_text("1/101968") == date(1968, 10, 1)
        assert get_date_from_numbered_text("10/11968") == date(1968, 1, 10)
        assert get_date_from_numbered_text("10/101968") == date(1968, 10, 10)
        # hyphen
        assert get_date_from_numbered_text("1-11968") == date(1968, 1, 1)
        assert get_date_from_numbered_text("1-101968") == date(1968, 10, 1)
        assert get_date_from_numbered_text("10-11968") == date(1968, 1, 10)
        assert get_date_from_numbered_text("10-101968") == date(1968, 10, 10)
        # underscore
        assert get_date_from_numbered_text("1_11968") == date(1968, 1, 1)
        assert get_date_from_numbered_text("1_101968") == date(1968, 10, 1)
        assert get_date_from_numbered_text("10_11968") == date(1968, 1, 10)
        assert get_date_from_numbered_text("10_101968") == date(1968, 10, 10)
        # de
        assert get_date_from_numbered_text("1 de 11968") == date(1968, 1, 1)
        assert get_date_from_numbered_text("1 de 101968") == date(1968, 10, 1)
        assert get_date_from_numbered_text("10 de 11968") == date(1968, 1, 10)
        assert get_date_from_numbered_text("10 de 101968") == date(1968, 10, 10)

    # only second separator
    def test_date_should_be_recognized_with_second_separator_only_when_four_char_parts(
        self,
    ):
        # whitespace
        assert get_date_from_numbered_text("11 1968") is None
        assert get_date_from_numbered_text("110 1968") is None
        assert get_date_from_numbered_text("101 1968") is None
        assert get_date_from_numbered_text("1010 1968") == date(1968, 10, 10)
        # slash
        assert get_date_from_numbered_text("11/1968") is None
        assert get_date_from_numbered_text("110/1968") is None
        assert get_date_from_numbered_text("101/1968") is None
        assert get_date_from_numbered_text("1010/1968") == date(1968, 10, 10)
        # hyphen
        assert get_date_from_numbered_text("11-1968") is None
        assert get_date_from_numbered_text("110-1968") is None
        assert get_date_from_numbered_text("101-1968") is None
        assert get_date_from_numbered_text("1010-1968") == date(1968, 10, 10)
        # underscore
        assert get_date_from_numbered_text("11_1968") is None
        assert get_date_from_numbered_text("110_1968") is None
        assert get_date_from_numbered_text("101_1968") is None
        assert get_date_from_numbered_text("1010_1968") == date(1968, 10, 10)
        # de
        assert get_date_from_numbered_text("11 de 1968") is None
        assert get_date_from_numbered_text("110 de 1968") is None
        assert get_date_from_numbered_text("101 de 1968") is None
        assert get_date_from_numbered_text("1010 de 1968") == date(1968, 10, 10)

    # no separator
    def test_date_should_be_recognized_without_separator_only_when_eight_char_length(
        self,
    ):
        assert get_date_from_numbered_text("0010022025") is None  # 001 de 002
        assert get_date_from_numbered_text("001022025") is None  # 001 de 02
        assert get_date_from_numbered_text("010022025") is None  # 01 de 002
        assert get_date_from_numbered_text("01022025") == date(2025, 2, 1)  # 01 de 02
        assert get_date_from_numbered_text("1022025") is None  # 1 de 02
        assert get_date_from_numbered_text("0122025") is None  # 01 de 2
        assert get_date_from_numbered_text("122025") is None  # 1 de 2

    # INCONSISTENCY
    def test_inexistent_date_text_should_return_none(self):
        # ano bissexto
        assert get_date_from_numbered_text("29 02 2025") is None
        assert get_date_from_numbered_text("30 02 2025") is None
        # 31th day month
        assert get_date_from_numbered_text("31 02 2025") is None
        assert get_date_from_numbered_text("31 04 2025") is None
        assert get_date_from_numbered_text("31 06 2025") is None
        assert get_date_from_numbered_text("31 09 2025") is None
        assert get_date_from_numbered_text("31 11 2025") is None
        # day > 31
        assert get_date_from_numbered_text("40 01 2025") is None
        assert get_date_from_numbered_text("50 01 2025") is None
        assert get_date_from_numbered_text("600 04 2025") is None
        assert get_date_from_numbered_text("7000 05 2025") is None
        # month > 12
        assert get_date_from_numbered_text("01 13 2025") is None
        assert get_date_from_numbered_text("01 14 2025") is None
        assert get_date_from_numbered_text("01 150 2025") is None
        assert get_date_from_numbered_text("01 1600 2025") is None


class TestGetDateFromMonthWrittenText:
    # INPUT / ARG
    def test_if_text_isnt_string_should_return_none(self):
        assert get_date_from_month_written_text(None) is None
        assert get_date_from_month_written_text(1.2) is None
        assert get_date_from_month_written_text([]) is None
        assert get_date_from_month_written_text((1, 2)) is None

    def test_if_text_is_empty_string_should_return_none(self):
        assert get_date_from_month_written_text("") is None

    # CONTENT
    # 2 separators
    def test_date_should_be_recognized_when_two_separators(self):
        assert get_date_from_month_written_text("23 novembro 2028") == date(
            2028, 11, 23
        )
        assert get_date_from_month_written_text("23/novembro/2028") == date(
            2028, 11, 23
        )
        assert get_date_from_month_written_text("23-novembro-2028") == date(
            2028, 11, 23
        )
        assert get_date_from_month_written_text("23_novembro_2028") == date(
            2028, 11, 23
        )
        assert get_date_from_month_written_text("23 de novembro de 2028") == date(
            2028, 11, 23
        )

    # only first separator
    def test_date_should_be_recognized_when_first_separator_only(self):
        assert get_date_from_month_written_text("03 outubro2000") == date(2000, 10, 3)
        assert get_date_from_month_written_text("03/outubro2000") == date(2000, 10, 3)
        assert get_date_from_month_written_text("03-outubro2000") == date(2000, 10, 3)
        assert get_date_from_month_written_text("03_outubro2000") == date(2000, 10, 3)
        assert get_date_from_month_written_text("03 de outubro2000") == date(
            2000, 10, 3
        )

    # only second separator
    def test_date_should_be_recognized_when_second_separator_only(self):
        assert get_date_from_month_written_text("23novembro 2028") == date(2028, 11, 23)
        assert get_date_from_month_written_text("23novembro/2028") == date(2028, 11, 23)
        assert get_date_from_month_written_text("23novembro-2028") == date(2028, 11, 23)
        assert get_date_from_month_written_text("23novembro_2028") == date(2028, 11, 23)
        assert get_date_from_month_written_text("23novembro de 2028") == date(
            2028, 11, 23
        )

    # no separator
    def test_date_should_be_recognized_without_separators(self):
        assert get_date_from_month_written_text("03fevereiro2025") == date(2025, 2, 3)

    ## de separator vs de dezembro
    def test_de_separator_shouldnt_conflict_with_dezembro(self):
        assert get_date_from_month_written_text("15 de dezembro de 1995") == date(
            1995, 12, 15
        )

        assert get_date_from_month_written_text("15de dezembro de 1995") == date(
            1995, 12, 15
        )
        assert get_date_from_month_written_text("15 dedezembro de 1995") == date(
            1995, 12, 15
        )
        assert get_date_from_month_written_text("15dedezembro de 1995") == date(
            1995, 12, 15
        )

        assert get_date_from_month_written_text("15 de dezembrode 1995") == date(
            1995, 12, 15
        )
        assert get_date_from_month_written_text("15 de dezembro de1995") == date(
            1995, 12, 15
        )
        assert get_date_from_month_written_text("15 de dezembrode1995") == date(
            1995, 12, 15
        )

        assert get_date_from_month_written_text("15dedezembrode1995") == date(
            1995, 12, 15
        )

    # INCONSISTENCY
    def test_inexistent_date_text_should_return_none(self):
        # ano bissexto
        assert get_date_from_month_written_text("29 fevereiro 2025") is None
        assert get_date_from_month_written_text("30 fevereiro 2025") is None
        # 31th day month
        assert get_date_from_month_written_text("31 fevereiro 2025") is None
        assert get_date_from_month_written_text("31 abril 2025") is None
        assert get_date_from_month_written_text("31 junho 2025") is None
        assert get_date_from_month_written_text("31 setembro 2025") is None
        assert get_date_from_month_written_text("31 novembro 2025") is None
        # day > 31
        assert get_date_from_month_written_text("40 janeiro 2025") is None
        assert get_date_from_month_written_text("50 janeiro 2025") is None
        assert get_date_from_month_written_text("600 janeiro 2025") is None
        assert get_date_from_month_written_text("7000 janeiro 2025") is None

    def test_if_recognizes_date_from_month_with_typo(self):
        assert get_date_from_month_written_text("8 de janiro de 2030") == date(
            2030, 1, 8
        )
        assert get_date_from_month_written_text("8 de feverero de 2030") == date(
            2030, 2, 8
        )
        assert get_date_from_month_written_text("8 de maro de 2030") == date(2030, 3, 8)
        assert get_date_from_month_written_text("8 de abriu de 2030") == date(
            2030, 4, 8
        )
        assert get_date_from_month_written_text("8 de maiio de 2030") == date(
            2030, 5, 8
        )
        assert get_date_from_month_written_text("8 de juno de 2030") == date(2030, 6, 8)
        assert get_date_from_month_written_text("8 de julo de 2030") == date(2030, 7, 8)
        assert get_date_from_month_written_text("8 de agosti de 2030") == date(
            2030, 8, 8
        )
        assert get_date_from_month_written_text("8 de setembu de 2030") == date(
            2030, 9, 8
        )
        assert get_date_from_month_written_text("8 de oubro de 2030") == date(
            2030, 10, 8
        )
        assert get_date_from_month_written_text("8 de novem de 2030") == date(
            2030, 11, 8
        )
        assert get_date_from_month_written_text("8 de zembro de 2030") == date(
            2030, 12, 8
        )


class TestGetMonthValue:
    # TEXT ARG
    def test_if_text_isnt_string_should_return_none(self):
        assert get_month_value(None) is None
        assert get_month_value("") is None
        assert get_month_value([]) is None

    def test_if_text_is_empty_string_should_return_none(self):
        assert get_month_value("") is None

    # CONTENT
    def test_if_whitespace_in_extremities_is_parsed_as_if_without_it(self):
        assert get_month_value("   janeiro    ") == 1

    def test_if_upper_case_is_ignored(self):
        assert get_month_value("JunHo") == 6
        assert get_month_value("jUlhO") == 7

    def test_if_text_with_diacritics_should_be_parsed_as_if_without_it(self):
        assert get_month_value("março") == 3
        assert get_month_value("máíó") == 5
        assert get_month_value("mâîô") == 5
        assert get_month_value("mãĩõ") == 5

    def test_if_world_length_less_than_3_char_returns_none(self):
        assert get_month_value("ja") is None
        assert get_month_value("fe") is None
        assert get_month_value("ma") is None
        assert get_month_value("ab") is None
        assert get_month_value("ma") is None
        assert get_month_value("ju") is None
        assert get_month_value("ag") is None
        assert get_month_value("se") is None
        assert get_month_value("ou") is None
        assert get_month_value("no") is None
        assert get_month_value("de") is None

    def test_if_ambiguous_cases_return_none(self):
        assert get_month_value("juho") is None  # could be junho or julho

    def test_if_numbered_text_returns_appropriate_int_only_when_month_value_exists(
        self,
    ):
        assert get_month_value("01") == 1
        assert get_month_value("02") == 2
        assert get_month_value("03") == 3
        assert get_month_value("04") == 4
        assert get_month_value("05") == 5
        assert get_month_value("06") == 6
        assert get_month_value("07") == 7
        assert get_month_value("08") == 8
        assert get_month_value("09") == 9
        assert get_month_value("10") == 10
        assert get_month_value("11") == 11
        assert get_month_value("12") == 12

        # month 13, 14, 15, etc, doesnt exist
        assert get_month_value("13") is None
        assert get_month_value("14") is None
        assert get_month_value("15") is None

    def test_if_common_abbreviation_is_recognized_correctly(self):
        assert get_month_value("jan") == 1
        assert get_month_value("fev") == 2
        assert get_month_value("mar") == 3
        assert get_month_value("abr") == 4
        assert get_month_value("mai") == 5
        assert get_month_value("jun") == 6
        assert get_month_value("jul") == 7
        assert get_month_value("ago") == 8
        assert get_month_value("set") == 9
        assert get_month_value("out") == 10
        assert get_month_value("nov") == 11
        assert get_month_value("dez") == 12

    def test_janeiro_recognition(self):
        # 1 letter is missing
        assert get_month_value("aneiro") == 1
        assert get_month_value("jneiro") == 1
        assert get_month_value("jaeiro") == 1
        assert get_month_value("janiro") == 1
        assert get_month_value("janero") == 1
        assert get_month_value("janeio") == 1
        # progressive missing letters
        assert get_month_value("janeir") == 1
        assert get_month_value("janei") == 1
        assert get_month_value("jane") == 1
        # letters position changed
        assert get_month_value("janiero") == 1
        assert get_month_value("janeior") == 1
        assert get_month_value("jnaeiro") == 1

    def test_junho_recognition(self):
        # 1 letter is missing
        assert get_month_value("unho") == 6
        assert get_month_value("jnho") == 6
        assert get_month_value("juno") == 6
        # progressive missing letters
        assert get_month_value("junh") == 6
        # letters position changed
        assert get_month_value("juhno") == 6
        assert get_month_value("jnuho") == 6
        assert get_month_value("junoh") == 6

    def test_julho_recognition(self):
        # 1 letter is missing
        assert get_month_value("ulho") == 7
        assert get_month_value("jlho") == 7
        assert get_month_value("julo") == 7
        # progressive missing letters
        assert get_month_value("julh") == 7
        # letters position changed
        # assert get_month_value("juhlo") == 7   # não passa
        # assert get_month_value("jluho") == 7   # não passa
        assert get_month_value("juloh") == 7
        # assert get_month_value("jolhu") == 7   # não passa

    def test_if_known_case_typos_are_fixed(self):  # real cases from spiders
        assert get_month_value("edicao") is None
        assert get_month_value("abril0") == 4
        assert get_month_value("junhoe") == 6
        assert get_month_value("agosoto") == 8
        assert get_month_value("dezembrbo") == 12
        assert get_month_value("setembo") == 9
        assert get_month_value("novembo") == 11
