from gazette.mapeadores.base.mapeadorsemantico import MapeadorSemantico


class MapeadorDeto(MapeadorSemantico):
    name = "mapeadordeto"

    def pattern_name(self):
        return "DETO"

    def valid_urls(self):
        return "vDETO"

    def urls_pattern(self, protocol, city, state_code):
        # casos conhecidos
        # http://www.auroradotocantins.to.gov.br/transparencia/diarioeletronico/
        # http://www.pontealtadobomjesus.to.gov.br/transparencia/diarioeletronico/

        return [
            f"{protocol}://www.{city}.{state_code}.gov.br/transparencia/diarioeletronico/"
        ]

    def validation(self, response):
        if "scMenuTHeaderFont" in response.text:
            return True
        return False
