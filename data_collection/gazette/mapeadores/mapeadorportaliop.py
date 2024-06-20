from gazette.mapeadores.base.mapeadornumerico import MapeadorNumerico


class MapeadorPortalIOP(MapeadorNumerico):
    name = "mapeadorportaliop"

    custom_settings = {"CONCURRENT_REQUESTS": 1, "DOWNLOAD_DELAY": 0.5}

    def pattern_name(self):
        return "PORTALIOP"

    def current_status(self):
        return "PORTALIOP_status"

    def urls_pattern(self, i):
        # casos conhecidos
        # https://www.portaliop.org.br/diariopref/?id=77
        # https://www.portaliop.org.br/diariopref/?id=78
        # https://www.portaliop.org.br/diariopref/?id=79

        return f"https://www.portaliop.org.br/diariopref/?id={i}"

    def num_max(self):
        return 3500

    def state(self):
        return ""

    def collect_metadata(self, response):
        rawname = response.xpath('//*[@id="logo"]/img').get()

        if "png" in rawname or "jpg" in rawname:
            return rawname, ""
        return None, None
