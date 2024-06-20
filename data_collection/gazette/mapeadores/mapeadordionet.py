from gazette.mapeadores.base.mapeadorsemantico import MapeadorSemantico


class MapeadorDionet(MapeadorSemantico):
    name = "mapeadordionet"

    def pattern_name(self):
        return "DIONET"

    def valid_urls(self):
        return "vDIONET"

    def current_status(self):
        return "DIONET_status"

    def urls_pattern(self, protocol, city, state_code):
        # casos conhecidos
        # https://diariodomunicipio.sjc.sp.gov.br/
        # https://do.corumba.ms.gov.br/
        # https://doe.jaru.ro.gov.br/

        return [
            f"{protocol}://diariodomunicipio.{city}.{state_code}.gov.br/",
            f"{protocol}://do.{city}.{state_code}.gov.br/",
            f"{protocol}://doe.{city}.{state_code}.gov.br/",
        ]

    def validation(self, response):
        if "icon-area-publicador p-3 mr-3 float-left" in response.text:
            return True
        return False

    def is_current(self, response):
        return "verificar"
