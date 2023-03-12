from scrapy import *
from bit28.items import Bit28Item


class SiteSpider(Spider):
    name = '28BitSpider'

    headers = {
        "authority": "28bit.ru",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "referer": "https://28bit.ru/",
        "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"102\", \"Google Chrome\";v=\"102\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
    }

    cookies = {
        "products_per_page": "90"
    }

    BASE_URL = 'https://28bit.ru'
    SHOP = '28bit.ru'

    def start_requests(self):
        urls = [
            'https://28bit.ru/category/protsessory/',
            'https://28bit.ru/category/videokarty/',
            'https://28bit.ru/category/materinskie-platy/',
            'https://28bit.ru/category/operativnaya-pamyat/',
            'https://28bit.ru/category/diski-ssd/',
            'https://28bit.ru/category/diski-hdd/',
            'https://28bit.ru/category/bloki-pitaniya/',
            'https://28bit.ru/category/korpusa/',
            'https://28bit.ru/category/sistemy-okhlazhdeniya/'
        ]

        for url in urls:
            yield Request(url=url, cookies=self.cookies, headers=self.headers, callback=self.parse)

    def parse(self, response):

        table = response.xpath("//div[@class='js-product-item product-list__item tile-gallery js-tile-gallery']").getall()
        for rows in table:
            row = Selector(text=rows)
            item = Bit28Item()
            item['link'] = self.BASE_URL + row.xpath("//a[@class='product-list__name']/@href").get()
            item['title'] = row.xpath("//a[@class='product-list__name']/text()").get().strip()
            item['price'] = row.xpath("//div[@class='product-list__price']/span/text()").get().strip()

            available = row.xpath("//div[@class='product-stock product-stock--none product-list__stock']/text()").get()
            item['available'] = '1'
            if available == 'Нет в наличии':
                item['available'] = '0'

            try:
                item['image'] = self.BASE_URL + row.xpath("//img[@class='js-product-preview-img']/@data-src").get()
            except TypeError:
                item['image'] = ''

            item['shop'] = self.SHOP
            item['sku'] = row.xpath("//div[@class='product-code product-list__code']/text()").get().strip()
            item['category'] = response.xpath("//h1[@class='category-name']/text()").get().split(' купить c доставкой в день заказа')[0]
            yield item

        next_page = response.xpath("//a[@class='inline-link']/@href")
        if next_page:
            next_page_url = self.BASE_URL + next_page[-1].get()
            yield Request(url=next_page_url, cookies=self.cookies, headers=self.headers, callback=self.parse)