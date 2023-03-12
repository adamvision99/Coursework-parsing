# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

#Опишем поля, которые будут на выходе
class DnsItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    available = scrapy.Field()
    price = scrapy.Field()
    link = scrapy.Field()
    image = scrapy.Field()
    sku = scrapy.Field()
    shop = scrapy.Field()
    category = scrapy.Field()

