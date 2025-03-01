import re
from urllib.parse import urlparse, urlunparse


class PatternsSpecifcs:
    def adiariosv1(entry, attributes):
        template_file = "adiariosv1.jinja"

        parsed_url = urlparse(entry["url"])
        replacements = {"path": "", "params": "", "query": "", "fragment": ""}
        attributes["base_url"] = urlunparse(parsed_url._replace(**replacements))
        attributes["domain"] = parsed_url.netloc.replace("www.", "")

        return template_file, attributes

    def adiariosv2(entry, attributes):
        template_file = "adiariosv2.jinja"

        parsed_url = urlparse(entry["url"])
        replacements = {"path": "", "params": "", "query": "", "fragment": ""}
        attributes["base_url"] = urlunparse(parsed_url._replace(**replacements))
        attributes["domain"] = parsed_url.netloc.replace("www.", "")

        return template_file, attributes

    # aratext

    def doem(entry, attributes):
        template_file = "doem.jinja"

        parsed_url = urlparse(entry["url"])
        attributes["state_city_url_part"] = re.search(
            r"/(.+)/diarios", parsed_url.path
        ).group(1)

        return template_file, attributes

    def dosp(entry, attributes):
        template_file = "dosp.jinja"
        attributes["url"] = entry["url"]

        return template_file, attributes


# instar
