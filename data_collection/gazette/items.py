import scrapy


class Gazette(scrapy.Item):
    date = scrapy.Field()
    edition_number = scrapy.Field()
    file_checksum = scrapy.Field()
    file_path = scrapy.Field()
    file_url = scrapy.Field()
    file_requests = scrapy.Field()
    is_extra_edition = scrapy.Field()
    public_entity_id = scrapy.Field()
    power = scrapy.Field()
    act_category = scrapy.Field()
    publishing_body = scrapy.Field()
    document_code = scrapy.Field()
    document_page = scrapy.Field()
    granularity = scrapy.Field()
    scraped_at = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    _validation = scrapy.Field()
