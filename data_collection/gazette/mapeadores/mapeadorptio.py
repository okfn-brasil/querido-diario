from gazette.mapeadores.base.mapeadorsemantico import MapeadorSemantico


class MapeadorPtio(MapeadorSemantico):
    name = "mapeadorptio"

    def pattern_name(self):
        return "PTIO"

    def valid_urls(self):
        return "vPTIO"

    def current_status(self):
        return "PTIO_status"

    def urls_pattern(self, protocol, city, state_code):
        # casos conhecidos
        # http://ap.portaldatransparencia.com.br/prefeitura/tartarugalzinho/
        # http://ba.portaldatransparencia.com.br/prefeitura/angical/
        # http://rj.portaldatransparencia.com.br/prefeitura/areal/

        return [f"http://{state_code}.portaldatransparencia.com.br/prefeitura/{city}/"]

    def validation(self, response):
        if "sistemas.tmunicipal.org.br/red" in response.text:
            if "data-caderno" in response.text:
                return True
        return False

    def is_current(self, response):
        rawdate = response.xpath('//*[@class="data-caderno hidden-phone"]/text()').get()

        if rawdate is None:
            return "vazio"
        elif "2024" in rawdate:
            return "atual"
        elif "20" in rawdate or "19" in rawdate:
            return "descontinuado"
