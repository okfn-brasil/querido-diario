import re


class RsPortoAlegre:
    END_OF_PAGE_MARKER = '\n\n\nhttp://www.portoalegre.rs.gov.br/dopa'
    EXEMPTIONS_ATTR_REGEX = r'^( +[A-ZÀ-Ÿ \-]+:)'

    def __init__(self, text, path):
        self.text = text
        self.path = path

    def pages(self):
        return self.text.split(self.END_OF_PAGE_MARKER)[:-1]

    def text_sections(self):
        return re.split(r'\n{3,}', self._contents())

    def exemption_sections(self):
        return [
            section
            for section in self.text_sections()
            if 'dispensa de licitação' in section.lower()
        ]

    def exemptions(self):
        items = []
        for section in self.exemption_sections():
            items.append(self.exemption(section))
        return items

    def exemption(self, section):
        lines = re.split(self.EXEMPTIONS_ATTR_REGEX, section, flags=re.MULTILINE)
        for index, line in enumerate(lines):
            is_header_line = re.match(self.EXEMPTIONS_ATTR_REGEX, line)
            if is_header_line:
                lines = lines[index:]
                break

        for index, line in enumerate(lines):
            is_header_line = re.match(self.EXEMPTIONS_ATTR_REGEX, line)
            is_last_section = index == len(lines) - 1
            if is_header_line:
                line = line[:-1]
            if is_last_section:
                footer = re.split(r'\n{2,}', line)
                line = footer[0].strip()
            lines[index] = re.sub(r'\s{2,}', ' ', line.strip())
        attributes = dict(zip(lines[0::2], lines[1::2]))
        attributes['section'] = section
        attributes['path'] = self.path
        return attributes

    def _contents(self):
        contents = ''
        for page in self.pages():
            contents += '\n'.join(page.split('\n')[3:-2])
        return contents
