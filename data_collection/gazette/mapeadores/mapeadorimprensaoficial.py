from gazette.mapeadores.base.mapeador import Mapeador


class MapeadorImprensaOficial(Mapeador):
    name = "mapeadorimprensaoficial"

    def pattern_name(self):
        return "IMPOFICIAL"

    def valid_urls(self):
        return "vIMPOFICIAL"

    def current_status(self):
        return "IMPOFICIAL_status"

    def urls_pattern(self, protocol, city, state_code):
        # casos conhecidos
        # http://sapeacu.ba.gov.br/ultimos-diarios/
        # http://pmgongogiba.imprensaoficial.org/ultimos-diarios/

        lista = [
            f"{protocol}://{city}.{state_code}.gov.br/ultimos-diarios/",
            f"{protocol}://pm{city}{state_code}.imprensaoficial.org/ultimos-diarios/",
        ]
        return lista

    def validation(self, response):
        if "imprensaoficial.org" in response.text:
            if "Edição" in response.text:
                return True
        return False

    def is_current(self, response):
        pass
