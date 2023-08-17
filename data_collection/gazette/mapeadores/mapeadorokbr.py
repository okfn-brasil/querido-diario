from gazette.mapeadores.base.mapeador import Mapeador


class MapeadorOKBR(Mapeador):
    name = "mapeadorokbr"

    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 30,
        "RETRY_ENABLED": False,
        "DOWNLOAD_DELAY": 1,
    }

    def pattern_name(self):
        return "GITHUB"

    def valid_urls(self):
        return "v"

    def current_status(self):
        return "TipoBase"

    def urls_pattern(self, protocol, city, state_code):
        # casos conhecidos
        # https://github.com/okfn-brasil/querido-diario/blob/main/data_collection/gazette/spiders/ap/ap_santana.py
        # https://github.com/okfn-brasil/querido-diario/blob/main/data_collection/gazette/spiders/mg/mg_carmo_da_cachoeira.py

        return [
            f"https://github.com/okfn-brasil/querido-diario/blob/main/data_collection/gazette/spiders/{state_code}/{state_code}_{city}.py"
        ]

    def city_name_generator(self, city_name):
        combination_list = []

        combination_list.append(self.blankspaces_to_underline(city_name))  # city_name

        return combination_list

    def validation(self, response):
        if "404 - page not found" in response.text:
            return False
        return True

    def is_current(self, response):
        if "BaseGazetteSpider" in response.text:
            return "BaseGazette"
        elif "AdminLTEGazetteSpider" in response.text:
            return "AdminLTE"
        elif "BaseAplusSpider" in response.text:
            return "Aplus"
        elif "DoemGazetteSpider" in response.text:
            return "Doem"
        elif "DospGazetteSpider" in response.text:
            return "Dosp"
        elif "FecamGazetteSpider" in response.text:
            return "Fecam"
        elif "ImprensaOficialSpider" in response.text:
            return "ImprensaOficial"
        elif "BaseInstarSpider" in response.text:
            return "Instar"
        elif "BaseMunicipioOnlineSpider" in response.text:
            return "MunicipioOnline"
        elif "BaseSiganetSpider" in response.text:
            return "Siganet"
        elif "SigpubGazetteSpider" in response.text:
            return "Sigpub"
        return "verificar"
