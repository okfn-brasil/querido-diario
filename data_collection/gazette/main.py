from scrapy import cmdline

city = 'sp_franca -a start_date=2020-11-01'
# city = 'rn_natal'

cmdline.execute(f"scrapy crawl {city}".split())
