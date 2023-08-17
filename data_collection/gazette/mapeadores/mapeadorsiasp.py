from gazette.mapeadores.base.mapeador import Mapeador


class MapeadorSiasp(Mapeador):
    name = "mapeadorsiasp"

    def pattern_name(self):
        return "SIASP"

    def valid_urls(self):
        return "vSIASP"

    def urls_pattern(self, protocol, city, state_code):
        # casos conhecidos
        # https://www.taboleirogrande.rn.gov.br/diariolista.php
        # https://www.joaodias.rn.gov.br/diariolista.php

        return [f"{protocol}://www.{city}.{state_code}.gov.br/diariolista.php"]

    def validation(self, response):
        if "siasp.com.br" in response.text:
            return True
        return False
