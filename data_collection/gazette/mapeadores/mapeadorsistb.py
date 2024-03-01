from gazette.mapeadores.base.mapeador import Mapeador


class MapeadorSistB(Mapeador):
    name = "mapeadorsistb"

    def pattern_name(self):
        return "SISTB"

    def valid_urls(self):
        return "vSISTB"

    def current_status(self):
        return "SISTB_status"

    def urls_pattern(self, protocol, city, state_code):
        # casos conhecidos
        # https://transparencia.altoalegredomaranhao.ma.gov.br/diario
        # https://transparencia.santaluzia.ma.gov.br/diario
        # https://bacuri.diariomunicipal.net.br/

        lista = [
            f"{protocol}://transparencia.{city}.{state_code}.gov.br/diario",
            f"{protocol}://{city}.diariomunicipal.net.br/",
        ]
        return lista

    def validation(self, response):
        if "Edições Anteriores" in response.text and 'id="datahora"' in response.text:
            return True
        return False

    def is_current(self, response):
        raw = response.xpath('//*[@id="myTable"]/tr[1]/td[2]/b/text()').get()

        if raw is None:
            return "vazio"
        elif "2024" in raw:
            return "atual"
        elif "20" in raw or "19" in raw:
            return "descontinuado"
        else:
            return "verificar"
