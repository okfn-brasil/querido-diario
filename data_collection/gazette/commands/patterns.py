import re
from urllib.parse import urlparse, urlunparse


def _get_domain(url):
    return urlparse(url).netloc.replace("www.", "")


def _get_raw_url(url):
    parsed_url = urlparse(url)
    replacements = {"path": "", "params": "", "query": "", "fragment": ""}
    return urlunparse(parsed_url._replace(**replacements))


class PatternsSpecifcs:
    def adiariosv1(spider_infos, attributes):
        template_file = "adiariosv1.jinja"
        attributes["base_url"] = _get_raw_url(spider_infos["url"])
        attributes["domain"] = _get_domain(spider_infos["url"])
        return template_file, attributes

    def adiariosv2(spider_infos, attributes):
        template_file = "adiariosv2.jinja"
        attributes["base_url"] = _get_raw_url(spider_infos["url"])
        attributes["domain"] = _get_domain(spider_infos["url"])
        return template_file, attributes

    def aratext(spider_infos, attributes):
        template_file = "aratext.jinja"
        attributes["url"] = spider_infos["url"]
        attributes["domain"] = _get_domain(spider_infos["url"])
        return template_file, attributes

    def doem(spider_infos, attributes):
        template_file = "doem.jinja"
        attributes["state_city_url_part"] = re.search(
            r"/(.+)/diarios", urlparse(spider_infos["url"]).path
        ).group(1)
        return template_file, attributes

    def dosp(spider_infos, attributes):
        template_file = "dosp.jinja"
        attributes["url"] = spider_infos["url"]
        return template_file, attributes

    def instar(spider_infos, attributes):
        template_file = "instar.jinja"
        attributes["base_url"] = spider_infos["url"]
        attributes["domain"] = _get_domain(spider_infos["url"])
        return template_file, attributes
