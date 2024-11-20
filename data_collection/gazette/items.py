import scrapy


class Gazette(scrapy.Item):
    date = scrapy.Field()
    edition_number = scrapy.Field()
    scraped_file_checksum = scrapy.Field()
    scraped_file_path = scrapy.Field()
    scraped_url = scrapy.Field()
    file_requests = scrapy.Field()
    is_extra_edition = scrapy.Field()
    public_entity_id = scrapy.Field()
    power = scrapy.Field()
    scraped_at = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    _validation = scrapy.Field()
    act_category = scrapy.Field()
    publishing_body = scrapy.Field()
    document = scrapy.Field()
    document_sequence = scrapy.Field()
    granularity = scrapy.Field()
    spider_name = scrapy.Field()
