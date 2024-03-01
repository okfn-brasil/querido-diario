from gazette.mapeadores.base.mapeador import Mapeador


class MapeadorIPM(Mapeador):
    name = "mapeadoripm"

    def pattern_name(self):
        return "IPM"

    def valid_urls(self):
        return "vIPM"

    def current_status(self):
        return "IPM_status"

    def urls_pattern(self, protocol, city, state_code):
        # casos conhecidos
        # http://www.ipmbrasil.org.br/DiarioOficial/ba/pmbarradomendes/diario

        return [
            f"{protocol}://www.ipmbrasil.org.br/DiarioOficial/{state_code}/pm{city}/diario",
            f"{protocol}://www.ipmbrasil.org.br/DiarioOficial/{state_code}/{city}/diario",
        ]

    def validation(self, response):
        if "ipmbrasil.org.br" in response.text:
            if "Diário Oficial Próprio" in response.text:
                if "Home?action=showMessage&message=" not in response.url:
                    return True
        return False

    def is_current(self, response):
        raw = response.xpath(
            '//*[@id="content-article"]/table/tbody/tr[1]/td[1]/text()'
        ).get()

        if raw is None:
            return "verificar"
        elif "2024" in raw:
            return "atual"
        elif "/20" in raw or "/19" in raw:
            return "descontinuado"
        else:
            return "vazio"
