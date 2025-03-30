import datetime as dt

import dateparser

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider
from gazette.utils.dates import YearMonthDate, monthly_sequence


class RsPortoAlegreSpider(BaseGazetteSpider):
    TERRITORY_ID = "4314902"
    name = "rs_porto_alegre"
    allowed_domains = ["portoalegre.rs.gov.br"]
    start_urls = ["http://www2.portoalegre.rs.gov.br/dopa/"]
    start_date = dt.date(2003, 9, 3)

    custom_settings = {"CONCURRENT_REQUESTS": 8}

    def parse(self, response):
        menu_years = response.css("ul#menucss > li")
        for menu_year in menu_years:
            menu_months = menu_year.xpath("./ul/li[not(contains(a/text(), 'Diário'))]")
            months_links = self._filter_months_of_interest(menu_months)
            yield from response.follow_all(months_links, callback=self.parse_month_page)

    def parse_month_page(self, response):
        editions = response.css("#conteudo a[href$='.pdf']:not(.gbox)")
        for edition in editions:
            text = edition.css("::text")
            date = self._extract_date(text)

            if date is None:
                continue

            if not self.start_date <= date <= self.end_date:
                continue

            is_extra_edition = "extra" in text.get().lower()
            url = response.urljoin(edition.attrib["href"])
            power = self._get_power_from_url(url)

            yield Gazette(
                date=date,
                file_urls=[url],
                is_extra_edition=is_extra_edition,
                power=power,
            )

    def _filter_months_of_interest(self, month_elements):
        months_of_interest = monthly_sequence(self.start_date, self.end_date)

        for month, month_element in enumerate(month_elements, start=1):
            year = int(month_element.css("a::text").re_first(r"\d{4}"))
            month_date = YearMonthDate(year, month)
            if month_date in months_of_interest:
                href = month_element.css("a").attrib["href"]
                yield href

    def _extract_date(self, text):
        common_pattern = text.re_first(r"\d+/\d+/\d+")
        full_written_pattern = text.re_first(r"\d{1,2}º?\s+de[\w\s]+\d{4}")
        marco_2010_pattern = text.re_first(r"marco2010[_\s]+(\d{2})marco10")

        if common_pattern:
            return dt.datetime.strptime(common_pattern, "%d/%m/%Y").date()
        elif full_written_pattern:
            full_written_pattern = full_written_pattern.replace("º", "")
            return dateparser.parse(full_written_pattern, languages=["pt"]).date()
        elif marco_2010_pattern:
            day = int(marco_2010_pattern)
            return dt.date(2010, 3, day)

    def _get_power_from_url(self, url):
        if "executivo" in url.lower():
            power = "executive"
        elif "legislativo" in url.lower():
            power = "legislative"
        else:
            power = "executive_legislative"
        return power
