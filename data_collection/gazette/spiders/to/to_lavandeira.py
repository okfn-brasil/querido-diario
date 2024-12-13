import datetime
import re
import urllib
from typing import Iterable

import scrapy
from scrapy import Request
from scrapy.selector import Selector
from scrapy.shell import inspect_response

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class ToLavandeira(BaseGazetteSpider):
    TERRITORY_ID = "1712157"
    name = "to_lavandeira"
    allowed_domains = ["lavandeira.to.gov.br"]
    start_date = datetime.date(2020, 1, 23)
    BASE_URL = "https://www.lavandeira.to.gov.br/transparencia"
    page_size = 10

    def start_requests(self) -> Iterable[Request]:
        data = {
            "script_case_init": "1",
            "opc": "muda_qt_linhas",
            "parm": str(self.page_size),
        }

        yield scrapy.Request(
            url=f"{self.BASE_URL}/diarioeletronico_grid_cliente",
            body=urllib.parse.urlencode(data),
            method="POST",
            callback=self.parse_table,
        )

    def parse_table(self, response):
        script_case_session = response.xpath(
            '//form[@name="form_ajax_redir_1"]//input[@name="script_case_session"]/@value'
        ).get()

        # Cada linha tem um link cujo href contem parametros para abrir o modal
        lines = response.xpath('//tr[starts-with(@id, "SC_ancor")]').getall()

        # O href e uma chamada dum metodo JS. Precisamos do terceiro parametro para continuar.
        # Este parametro tem um sufixo hexadecimal
        modal_request_params = []
        for line in lines:
            modal_param_match = re.search(
                r"(@SC_par@\d+?@SC_par@diarioeletronico_grid_cliente@SC_par@.+?)'", line
            )

            if modal_param_match:
                date_str = (
                    Selector(text=line)
                    .xpath('//span[starts-with(@id, "id_sc_field_dataedicao_")]/text()')
                    .get()
                )
                doc_date = datetime.datetime.strptime(date_str, "%d/%m/%Y").date()

                doc_edition = (
                    Selector(text=line)
                    .xpath(
                        '//span[starts-with(@id, "id_sc_field_numeroedicao_")]/text()'
                    )
                    .get()
                )

                modal_request_params.append(
                    {
                        "modal_param": modal_param_match.group(1),
                        "doc_date": doc_date,
                        "doc_edition": doc_edition,
                    }
                )

        # loop modal_request_params_list
        modal_params = modal_request_params[0]

        modal_url = f"""
            {self.BASE_URL}/diarioeletronico_form_cliente?
            &script_case_session={script_case_session}
            &nmgp_outra_jan=true
            &nmgp_url_saida=modal
            &SC_lig_apl_orig=diarioeletronico_grid_cliente
            &nmgp_parms={modal_params['modal_param']}
        """

        yield scrapy.Request(
            url=modal_url,
            callback=self.parse_modal,
            cb_kwargs=modal_params,
        )

    def parse_modal(self, response, doc_date, doc_edition, modal_param):
        inspect_response(response, self)
        # Extraia o href do link dentro do <div id="id_sc_loaded_anexo">
        script_case_init = response.xpath(
            '//form[@name="F1"]//input[@name="script_case_init"]/@value'
        ).get()

        doc_href = response.xpath('//div[@id="id_sc_loaded_anexo"]//a/@href').get()

        # Extraia o segundo parâmetro da chamada JavaScript
        doc_name = None
        if doc_href:
            match = re.search(r"'documento_db', '(.+?)'", doc_href)
            if match:
                doc_name = match.group(1)

        is_extra_edition = False

        gazette_url = f"""
            {self.BASE_URL}/diarioeletronico_form_cliente/diarioeletronico_form_cliente_doc.php?
            script_case_init={script_case_init}
            &nm_cod_doc=documento_db
            &nm_nome_doc={doc_name}
            &nm_cod_apl=diarioeletronico_form_cliente
        """

        yield Gazette(
            date=doc_date,
            edition_number=doc_edition,
            is_extra_edition=is_extra_edition,
            file_urls=[gazette_url],
            power="executive",
        )
