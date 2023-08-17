from gazette.mapeadores.base.mapeador import Mapeador


class MapeadorIPM(Mapeador):
    name = "mapeadoripm"

    def pattern_name(self):
        return "IPM"

    def valid_urls(self):
        return "vIPM"

    def urls_pattern(self, protocol, city, state_code):
        # casos conhecidos
        # http://www.ipmbrasil.org.br/DiarioOficial/ba/pmbarradomendes/diario

        return [
            f"{protocol}://www.ipmbrasil.org.br/DiarioOficial/{state_code}/pm{city}/diario"
        ]

    def validation(self, response):
        if "ipmbrasil.org.br" in response.text:
            if "Diário Oficial Próprio" in response.text:
                if "Home?action=showMessage&message=" not in response.url:
                    return True
        return False
