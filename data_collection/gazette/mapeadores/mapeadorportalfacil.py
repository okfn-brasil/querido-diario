import re

import scrapy

from gazette.mapeadores.base.mapeadorsemantico import MapeadorSemantico


class MapeadorPortalFacil(MapeadorSemantico):
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    }

    name = "mapeadorportalfacil"

    def pattern_name(self):
        return "PORTALFACIL"

    def valid_urls(self):
        return "vPORTALFACIL"

    def current_status(self):
        return "PORTALFACIL_status"

    def urls_pattern(self, protocol, city, state_code):
        # casos conhecidos
        # https://www.manhuacu.mg.gov.br/diario-eletronico
        # https://www.saojosederibamar.ma.gov.br/diario-eletronico

        return [f"{protocol}://www.{city}.{state_code}.gov.br/diario-eletronico"]

    def validation(self, response):
        if "portalfacil.com.br" in response.text:
            if "pagina-nao-encontrada" not in response.url:
                return True
        return False

    def parse(self, response, index):
        if self.validation(response):
            if response.url not in self.territories[index][self.pattern_name()]:
                self.territories[index][self.pattern_name()].append(response.url)

            rawpath = response.xpath('//*[@id="Form1"]/script[13]').get()
            urlpath = re.search(r'src="(.*)"><', rawpath).group(1)

            headers = {
                # "Accept": "*/*",
                # "Accept-Encoding": "gzip, deflate, br",
                # "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
                # # "Cache-Control": "no-cache",
                # # "Content-Length": 140,
                # "Content-Type": "text/plain; charset=UTF-8",
                # "Origin": "https://www.aiquara.ba.gov.br",
                # # "Pragma": "no-cache",
                # "Referer": "https://www.aiquara.ba.gov.br/diario-eletronico",
                # "sec-ch-ua":'"Chromium";v="121", "Not A(Brand";v="99"',
                # "sec-ch-ua-mobile": "?0",
                # "sec-ch-ua-platform": "Linux",
                # "Sec-Fetch-Dest": "empty",
                # "Sec-Fetch-Mode": "cors",
                # "Sec-Fetch-Site": "same-origin",
                "X-AjaxPro-Method": "GetMaiorDataDiario"
            }

            body = '{"cdCadernoDiario":-1,"dtDiario_menor":null,"dtDiario_maior":null,"dsPalavraChave":"","nuEdicao":-1}'

            yield scrapy.Request(
                url=response.urljoin(urlpath),
                method="POST",
                body=body,
                headers=headers,
                meta={"handle_httpstatus_list": [400]},
                callback=self.is_current,
                cb_kwargs=dict(index=index),
            )

        elif response.url not in self.territories[index][self.valid_urls()]:
            self.territories[index][self.valid_urls()].append(response.url)

    def is_current(self, response, index):
        if "2024" in response.text:
            iscurrent = "atual"
        elif "20" in response.text or "19" in response.text:
            iscurrent = "descontinuado"
        else:
            iscurrent = "vazio"

        self.territories[index][self.current_status()].append(iscurrent)
