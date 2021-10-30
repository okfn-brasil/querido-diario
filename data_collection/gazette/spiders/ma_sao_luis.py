from ast import literal_eval
from datetime import date, timedelta
from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class MaSaoLuisSpider(BaseGazetteSpider):
    TERRITORY_ID = '2111300'
    name = 'ma_sao_luis'
    allowed_domains = ['sistemas.semad.saoluis.ma.gov.br']
    start_url = 'http://sistemas.semad.saoluis.ma.gov.br/easysearch/easysearch_searchview/gwtengine'
    start_date = date(1993, 1, 1)

    ENDPOINT_URL = "http://sistemas.semad.saoluis.ma.gov.br/easysearch/easysearch_searchview/gwtengine"
    GWT_PERMUTATION = "ED8E2EB15828804103DA822266394399"
    EXTRA_EDITION_TEXT = "SUPLEMENT"
    PDF_URL = "http://sistemas.semad.saoluis.ma.gov.br/easysearch/cachedownloader?collection=default&docId=%s&fieldName=Download&extension=pdf#q="

    MONTHS = [
        'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
        'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
    ]

    # GWT RCP Payloads
    RPC_CONFIG_PAYLOAD = '7|0|7|http://sistemas.semad.saoluis.ma.gov.br/easysearch/easysearch_searchview/|' \
        '39DA7FE6E21AADE8C06FBA64A74B9DD9|br.com.dataeasy.easysearch.client.core.ManagerService|' \
        'execute|br.com.dataeasy.easysearch.client.core.ClientCommand|' \
        'br.com.dataeasy.easysearch.client.command.LoadConfigCmd/2753954244|' \
        'br.com.dataeasy.easysearch.shared.imp.ViewMode/3808824691' \
        '|1|2|3|4|1|5|6|1|7|1|'

    RPC_BOOTSTRAP_PAYLOAD = '7|0|7|http://sistemas.semad.saoluis.ma.gov.br/easysearch/easysearch_searchview/|' \
        '39DA7FE6E21AADE8C06FBA64A74B9DD9|br.com.dataeasy.easysearch.client.core.ManagerService|' \
        'execute|br.com.dataeasy.easysearch.client.core.ClientCommand|' \
        'br.com.dataeasy.easysearch.client.command.BootstrapCmd/578233705|' \
        'default|1|2|3|4|1|5|6|7|0|'

    RPC_SEARCH_PAYLOAD = '7|0|72|' \
        'http://sistemas.semad.saoluis.ma.gov.br/easysearch/easysearch_searchview/|' \
        '39DA7FE6E21AADE8C06FBA64A74B9DD9|' \
        'br.com.dataeasy.easysearch.client.core.ManagerService|' \
        'execute|' \
        'br.com.dataeasy.easysearch.client.core.ClientCommand|' \
        'br.com.dataeasy.easysearch.client.command.SearchRequestCmd/365718362|' \
        'default|' \
        'br.com.dataeasy.easysearch.shared.imp.SerialSearchRequest/182647667|' \
        'java.util.ArrayList/4159755760|' \
        'br.com.dataeasy.easysearch.shared.imp.Queries$FacetOr/921245615|' \
        'Data do diário|' \
        '[Lbr.com.dataeasy.easysearch.shared.IFilterQuery;/1566555152|' \
        'br.com.dataeasy.easysearch.shared.imp.FacetFieldFilter/3600436613|' \
        'ctr_api_Data_do_diário_dt_ctr_level3_tx_fc|' \
        '%s|' \
        'tag116|' \
        'br.com.dataeasy.easysearch.shared.imp.Operator/3082263444|' \
        'tag117|' \
        'java.util.HashMap/1797211028|' \
        'java.lang.String/2004016611|' \
        'br.com.dataeasy.easysearch.shared.imp.SerialSearchRequest$ProjectField|' \
        'br.com.dataeasy.easysearch.shared.imp.SerialSearchRequest$ProjectField/1523921243|' \
        'br.com.dataeasy.easysearch.shared.imp.TypeSupport/2084692144|' \
        'Download|Número do diário|Suplemento|Visualizar|' \
        'br.com.dataeasy.easysearch.shared.imp.SerialSearchRequest$HlField|' \
        'br.com.dataeasy.easysearch.shared.imp.SerialSearchRequest$HlField/2000415408|' \
        'br.com.dataeasy.easysearch.shared.imp.SerialSearchRequest$HlFragSize|' \
        'br.com.dataeasy.easysearch.shared.imp.SerialSearchRequest$HlFragSize/4076120198|' \
        'br.com.dataeasy.easysearch.shared.imp.SerialSearchRequest$SortField|' \
        'br.com.dataeasy.easysearch.shared.imp.SerialSearchRequest$SortField/4171213499|' \
        'br.com.dataeasy.easysearch.shared.SortMode/3550216510|' \
        'br.com.dataeasy.easysearch.shared.imp.SerialSearchRequest$FilterBy|' \
        'br.com.dataeasy.easysearch.shared.imp.SerialSearchRequest$FilterBy/3352297292|' \
        'br.com.dataeasy.easysearch.shared.imp.SerialSearchRequest$FacetMinCount|' \
        'br.com.dataeasy.easysearch.shared.imp.SerialSearchRequest$FacetMinCount/1503396037|' \
        'br.com.dataeasy.easysearch.shared.imp.SerialSearchRequest$FacetLimit|' \
        'br.com.dataeasy.easysearch.shared.imp.SerialSearchRequest$FacetLimit/2004551114|' \
        'br.com.dataeasy.easysearch.shared.imp.SerialSearchRequest$FacetTaxonomy|' \
        'br.com.dataeasy.easysearch.shared.imp.SerialSearchRequest$FacetTaxonomy/1542976096||' \
        'br.com.dataeasy.easysearch.shared.imp.SerialSearchRequest$PagingFrom|' \
        'br.com.dataeasy.easysearch.shared.imp.SerialSearchRequest$PagingFrom/2644311692|' \
        'br.com.dataeasy.easysearch.shared.imp.SerialSearchRequest$PageSize|' \
        'br.com.dataeasy.easysearch.shared.imp.SerialSearchRequest$PageSize/4271829286|' \
        'br.com.dataeasy.easysearch.shared.imp.SerialSearchRequest$FacetFieldByExclude|' \
        'br.com.dataeasy.easysearch.shared.imp.SerialSearchRequest$FacetFieldByExclude/4260176092|' \
        'br.com.dataeasy.easysearch.shared.imp.SerialSearchRequest$FacetOffsetField|' \
        'br.com.dataeasy.easysearch.shared.imp.SerialSearchRequest$FacetOffsetField/4030967082|' \
        'br.com.dataeasy.easysearch.shared.imp.SerialSearchRequest$FacetLimitField|' \
        'br.com.dataeasy.easysearch.shared.imp.SerialSearchRequest$FacetLimitField/3266405597|' \
        'br.com.dataeasy.easysearch.shared.imp.SerialSearchRequest$FacetSortField|' \
        'br.com.dataeasy.easysearch.shared.imp.SerialSearchRequest$FacetSortField/2435273722|' \
        'br.com.dataeasy.easysearch.shared.imp.FacetSortMode/4255894897|' \
        'br.com.dataeasy.easysearch.shared.imp.SerialSearchRequest$FacetQueryByFilterLabel|' \
        'br.com.dataeasy.easysearch.shared.imp.SerialSearchRequest$FacetQueryByFilterLabel/3534346405|' \
        'Diário Oficial - De Hoje|' \
        'br.com.dataeasy.easysearch.shared.imp.EvaluatorQuery/2658882158|' \
        '${field:Data do diário}:(NOW/DAY)|tag1|' \
        'Diário Oficial - Últimos 7 dias|${field:Data do diário}:[NOW/DAY-7DAYS TO NOW/DAY]|tag2|' \
        'Diário Oficial - Do Mês|${field:Data do diário}:[NOW/MONTH TO NOW/DAY]|tag3|' \
        'Diário Oficial - Do Ano|${field:Data do diário}:[NOW/YEAR TO NOW/DAY]|tag4|' \
        '*:*' \
        '|1|2|3|4|1|5|6|7|8|9|1|10|11|12|1|13|11|14|15|0|16|17|1|0|18|0|19|15|20|21|9|6|' \
        '22|11|23|10|22|24|23|14|22|25|23|5|22|26|-16|22|27|23|15|22|27|-14|20|28|9|6|29|' \
        '11|-12|29|24|-14|29|25|-16|29|26|-16|29|27|-19|29|27|-14|20|30|9|1|31|250|20|32|' \
        '9|1|33|11|34|1|-12|20|35|9|1|36|-4|20|37|9|1|38|1|20|39|9|1|40|12|20|41|9|1|42|' \
        '2147483647|43|20|44|9|1|45|0|20|46|9|1|47|100|20|48|9|1|49|0|26|26|-16|20|50|9|1|' \
        '51|26|0|-16|20|52|9|1|53|26|12|-16|20|54|9|1|55|26|-16|56|1|20|57|9|4|58|59|60|' \
        '61|0|62|0|58|63|60|64|0|65|0|58|66|60|67|0|68|0|58|69|60|70|0|71|0|0|72|0|0|0|0|'

    START_EDITION_MARK = 'api_Tamanho_do_arquivo_lg;'

    def start_requests(self):
        """Requests all days since the beginning."""
        begin = self.start_date
        end = self.end_date

        for day in range((end - begin).days):
            search_date = begin + timedelta(day)
            # ignore weekends
            if search_date.weekday() == 5 or search_date.weekday() == 6:
                continue

            yield self._send_gwt_request(
                self.RPC_CONFIG_PAYLOAD,
                meta={"date": search_date, "cookiejar": search_date.strftime('%Y%m%d')},
                callback=self.bootstrap)

    def bootstrap(self, response):
        yield self._send_gwt_request(
            self.RPC_BOOTSTRAP_PAYLOAD,
            meta=response.meta,
            callback=self.search_by_date
        )

    def search_by_date(self, response):
        date = response.meta['date']
        date_formatted = '%d»%s»%d' % (
            date.year,
            self.MONTHS[date.month - 1],
            date.day
        )

        yield self._send_gwt_request(
            self.RPC_SEARCH_PAYLOAD % (date_formatted),
            meta=response.meta,
            callback=self.parse
        )

    def _send_gwt_request(self, body, meta, callback):
        headers = {
            'X-GWT-Module-Base': self.ENDPOINT_URL,
            'X-GWT-Permutation': self.GWT_PERMUTATION,
            'Content-Type': 'text/x-gwt-rpc; charset=utf-8'
        }

        request = Request(
            self.ENDPOINT_URL,
            method="POST",
            body=body,
            meta=meta,
            headers=headers,
            callback=callback,
            dont_filter=True
        )

        return request


    def parse(self, response):
        body = response.body
        if body[:4] != b'//OK':
            # should be a exception
            raise "Error talking with RPC backend"

        content = self.decode(body)
        if content is None:
            return

        results = self.group_results(content)

        for result in results:
            yield Gazette(
                date=response.meta['date'],
                edition_number=result['number'],
                file_urls=[self.PDF_URL % (result['id'])],
                is_extra_edition=result['extra'],
                power="executive",
            )

    def decode(self, body):
        body = body[4:]
        body = body.decode('utf-8')
        # decode the string
        try:
            return literal_eval(body)
        except SyntaxError:
            return None

    def group_results(self, content):
        strings = self.get_strings(content)

        idxs = []
        for (i, entry) in enumerate(strings):
            if self.START_EDITION_MARK in entry:
                idxs.append(i)

        editions = []

        for idx in idxs:
            extra = strings[idx + 1] == 'Sim'
            if extra:
                idx = idx + 1

            number = strings[idx + 2]
            text = strings[idx + 3]
            id = strings[idx + 4]

            editions.append({
                'extra': extra,
                'id': id,
                'text': text,
                'number': number
            })

        return editions

    def get_strings(self, data):
        candidates = data[-3]

        stringClass = [c for c in candidates if c.startswith('java.lang.String/')]
        stringClass = stringClass[0]

        strIdx = candidates.index(stringClass) + 1
        ordered = []
        begin = 0

        while strIdx in data[begin + 1:]:
            idx = data.index(strIdx, begin + 1)
            pointer_data = data[idx - 1] - 1

            ordered.append(candidates[pointer_data].replace("\n", '\\n'))

            begin = idx

        return ordered

