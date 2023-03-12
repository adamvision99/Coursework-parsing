# Import library
from scrapy import *
from citilink.items import CitilinkItem

# Create Spider class
class itemSpider(Spider):
    # Name of spider
    name = 'CitilinkSpider'

    headers = {
        "authority": "www.citilink.ru",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-language": "ru,en-GB;q=0.9,en-US;q=0.8,en;q=0.7",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "referer": "https://www.citilink.ru/catalog/videokarty/?p=1&view_type=list",
        "sec-ch-ua": "\".Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"103\", \"Chromium\";v=\"103\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
    }

    cookies = {
        "_tuid": "97322101dbb0effd9209c967a63740b08170d5b8о",
        "old_design": "0",
        "is_show_welcome_mechanics": "1",
        "ab_test": "90x10v4%3A1%7Creindexer%3A2%7Cnew_designv10%3A2%7Cnew_designv13%3A1%7Cproduct_card_design%3A3%7Cdynamic_yield%3A3%7Cwelcome_mechanics%3A4%7Cdummy%3A20",
        "ab_test_analytics": "90x10v4%3A1%7Creindexer%3A2%7Cnew_designv10%3A2%7Cnew_designv13%3A1%7Cproduct_card_design%3A3%7Cdynamic_yield%3A3%7Cwelcome_mechanics%3A4%7Cdummy%3A20",
        "_dy_csc_ses": "t",
        "_space": "srt_cl%3A",
        "_pcl": "eW5i2ydF2V6oKA==",
        "_dy_ses_load_seq": "17457%3A1658529598024",
        "_dy_soct": "1017570.1030352.1658523403*1015299.1026208.1658523403*1025689.1050382.1658529598*1033770.1068198.1658529598*1036008.1075335.1658529598*1057924.1147253.1658529598*1060952.1157758.1658529598*1068296.1183150.1658529598*1008131.1012968.1658529598"
    }

    start_urls = [
         'https://www.citilink.ru/catalog/platformy-dlya-sborki-pk/',
         'https://www.citilink.ru/catalog/processory/',
         'https://www.citilink.ru/catalog/sistemy-ohlazhdeniya-kompyutera/',
         'https://www.citilink.ru/catalog/sistemy-ohlazhdeniya-processora/',
         'https://www.citilink.ru/catalog/sistemy-ohlazhdeniya-korpusa/',
         'https://www.citilink.ru/catalog/materinskie-platy/',
         'https://www.citilink.ru/catalog/moduli-pamyati/',
         'https://www.citilink.ru/catalog/videokarty/',
         'https://www.citilink.ru/catalog/bloki-pitaniya/',
         'https://www.citilink.ru/catalog/korpusa/',
         'https://www.citilink.ru/catalog/zvukovye-karty/',
         'https://www.citilink.ru/catalog/opticheskie-privody/',
         'https://www.citilink.ru/catalog/kontrollery-dlya-pk/'
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, method='GET', dont_filter=True, cookies=self.cookies, headers=self.headers)

    # Parses the website
    def parse(self, response):
        tables = response.xpath(
            "//div[@class='product_data__gtm-js product_data__pageevents-js ProductCardHorizontal js--ProductCardInListing js--ProductCardInWishlist']").getall()
        all_items = []
        for row in tables:
            item = CitilinkItem()
            row_item = Selector(text=row)
            available = row_item.xpath(
                "//a[@class='ProductDeliveryInfo__delivery-info-link js--ProductDeliveryInfo__delivery-info-link js--ProductCardInListing__delivery-date  Link js--Link Link_type_dotted' and @data-type='stock']/text()").get()
            delivery = row_item.xpath("//div[@class='ProductDeliveryInfo__stock-info']").get()
            if available or delivery:
                item['available'] = '1'
                item['price'] = row_item.xpath(
                    "//span[@class='ProductCardHorizontal__price_current-price js--ProductCardHorizontal__price_current-price ']/text()").get().strip()
            else:
                item['available'] = '0'
                item['price'] = ''

            item['title'] = ' '.join(row_item.xpath(
                "//a[@class='ProductCardHorizontal__title  Link js--Link Link_type_default']/text()").get().split())
            item['link'] = 'https://www.citilink.ru' + row_item.xpath(
                "//a[@class='ProductCardHorizontal__title  Link js--Link Link_type_default']").attrib['href']
            item['image'] = row_item.xpath(
                "//div[@class='ProductCardHorizontal__picture-hover_part js--ProductCardInListing__picture-hover_part']").attrib[
                'data-src']
            item['sku'] = item['link'].split('-')[-1].replace('/', '')
            item['category'] = response.xpath('//h1/text()').get().strip()

            yield item

        next_page = response.xpath('//a[@class="js--PaginationWidget__page PaginationWidget__arrow js--PaginationWidget__arrow PaginationWidget__arrow_right"]')
        if next_page:
            next_page_url = response.urljoin(f'?p={next_page.attrib["data-page"]}&view_type=list')
            yield Request(url=next_page_url, method='GET', dont_filter=True, cookies=self.cookies, headers=self.headers)