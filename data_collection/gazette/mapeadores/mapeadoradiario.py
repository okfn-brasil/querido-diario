from gazette.mapeadores.base.mapeador import Mapeador


class MapeadorAdiario(Mapeador):
    name = "mapeadoradiario"

    custom_settings = {
        "CONCURRENT_REQUESTS": 100,
        "RETRY_ENABLED": False,
    }

    def pattern_name(self):
        return "ADIARIO"

    def valid_urls(self):
        return "vADIARIO"

    def current_status(self):
        return "ADIARIO_status"

    def urls_pattern(self, protocol, city, state_code):
        # casos conhecidos
        # https://www.buriticupu.ma.gov.br/diariooficial.php
        # https://transparencia.cordeiro.rj.gov.br/jornal.php
        # https://www.crateus.ce.gov.br/diario.php

        lista = [
            f"{protocol}://www.{city}.{state_code}.gov.br/diariooficial.php",
            f"{protocol}://transparencia.{city}.{state_code}.gov.br/jornal.php",
            f"{protocol}://www.{city}.{state_code}.gov.br/diario.php",
            f"{protocol}://www.{city}.{state_code}.gov.br/diariolista.php",
        ]

        return lista

    def validation(self, response):
        if "assesi.com.br" in response.text or "siasp.com.br" in response.text:
            return True
        return False

    def is_current(self, response):
        if "transparencia" in response.url:
            if "'Exercício'>2024</td>" in response.text:
                return "atual"
            else:
                return "verificar"

        elif "diario.php" in response.url or "diariolista.php" in response.url:
            rawdate = response.xpath(
                '//*[@id="ancora"]/section[2]/div/div/div[3]/div/div[2]/div/a/h4/div/div/text()'
            ).get()

        elif "diariooficial.php" in response.url:
            rawdate = response.xpath('//*[@id="diario_lista"]/span/strong/text()').get()

        if rawdate is None:
            return "vazio"
        if "2024" in rawdate:
            return "atual"
        else:
            return "descontinuado"
