from importlib.metadata import version
from pathlib import Path

import yaml


def test_scrapy_cloud_extension_is_compatible_with_scrapy():
    from sh_scrapy.extension import HubstorageExtension

    config_path = Path(__file__).parents[1] / "scrapinghub.yml"
    config = yaml.safe_load(config_path.read_text())

    assert config["stack"] == "scrapy:2.14-20260326"
    assert version("scrapy") == "2.14.2"
    assert version("scrapinghub-entrypoint-scrapy") == "0.18.1"
    assert HubstorageExtension is not None
