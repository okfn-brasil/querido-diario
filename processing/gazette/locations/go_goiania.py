import re

from .base_parser import BaseParser


class GoGoiania(BaseParser):
    EXEMPTIONS_ATTR_REGEX = r'^( *\-[A-ZÀ-Ÿ \-]+:)'

    def pages(self):
        return re.split(r'Página \d+ de \d+', self.text)[1:]

    def bidding_exemption_sections(self):
        for section in self.pages():
            text = section.lower()
            if ('extrato de ato de dispensa de licitação' in text) or (
                'termo de dispensa de licitação n' in text
            ):
                yield section

    def bidding_exemptions(self):
        for section in self.bidding_exemption_sections():
            yield {'data': self.bidding_exemption(section), 'source_text': section}

    def bidding_exemption(self, section):
        section = section.replace(u'\uf02d', '-')
        lines = re.split(self.EXEMPTIONS_ATTR_REGEX, section, flags=re.MULTILINE)
        if len(lines) > 1:
            lines = lines[1:]
            lines[-1] = lines[-1].split('\n\n')[0]
            keys = [re.match(r'^\s*\- (.+):$', key)[1] for key in lines[0::2]]
            values = [re.sub(r'\s{2,}', ' ', value.strip()) for value in lines[1::2]]
            return dict(zip(keys, values))

        else:
            return {}
