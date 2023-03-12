# Import library
import time

from scrapy import *
from dns.items import DnsItem
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

counter = 1


# Create Spider class
class itemSpider(Spider):
    # Name of spider
    name = 'DNSSpider'

    start_urls = [
        'https://www.dns-shop.ru/catalog/17a899cd16404e77/processory/',
        'https://www.dns-shop.ru/catalog/17a89a0416404e77/materinskie-platy/',
        'https://www.dns-shop.ru/catalog/17a89aab16404e77/videokarty/',
        'https://www.dns-shop.ru/catalog/17a89a3916404e77/operativnaya-pamyat-dimm/',
        'https://www.dns-shop.ru/catalog/17a9b91b16404e77/operativnaya-pamyat-so-dimm/',
        'https://www.dns-shop.ru/catalog/17a9cc2d16404e77/kulery-dlya-processorov/',
        'https://www.dns-shop.ru/catalog/17a9cc9816404e77/sistemy-zhidkostnogo-oxlazhdeniya/',
        'https://www.dns-shop.ru/catalog/17a9cf0216404e77/ventilyatory-dlya-korpusa/',
        'https://www.dns-shop.ru/catalog/17a9cccc16404e77/termointerfejsy/',
        'https://www.dns-shop.ru/catalog/17a9d15416404e77/krepleniya-dlya-sistem-oxlazhdeniya/',
        'https://www.dns-shop.ru/catalog/46a6ee18ae77e78a/vodobloki/',
        'https://www.dns-shop.ru/catalog/c337d10545a1d894/radiatory-svo/',
        'https://www.dns-shop.ru/catalog/2cacbd38aaea1804/pompy-svo/',
        'https://www.dns-shop.ru/catalog/0448014d9ef2e443/rezervuary-svo/',
        'https://www.dns-shop.ru/catalog/36ca7a16b10e23fd/trubki-i-shlangi/',
        'https://www.dns-shop.ru/catalog/7dd2f94fbd40b838/fitingi-dlya-svo/',
        'https://www.dns-shop.ru/catalog/d9afd9ed4713ecfd/zhidkost-dlya-oxlazhdeniya/',
        'https://www.dns-shop.ru/catalog/ba01d15ff8c9184b/bekplejty-dlya-videokart/',
        'https://www.dns-shop.ru/catalog/6587106ffac24148/krepleniya-dlya-svo/',
        'https://www.dns-shop.ru/catalog/f57ceff4e49d10ec/instrumenty-dlya-raboty-s-svo/',
        'https://www.dns-shop.ru/catalog/17a9cfa016404e77/sistemy-oxlazhdeniya-videokarty/',
        'https://www.dns-shop.ru/catalog/85fe8b0e83901664/termoprokladki/',
        'https://www.dns-shop.ru/catalog/17a9d07a16404e77/sistemy-oxlazhdeniya-chipseta/',
        'https://www.dns-shop.ru/catalog/17a89a6e16404e77/radiatory-dlya-pamyati/',
        'https://www.dns-shop.ru/catalog/17a9cfd716404e77/radiatory-dlya-ssd-m2/',
        'https://www.dns-shop.ru/catalog/b37626c35ecf3604/sistemy-podsvetki/',
        'https://www.dns-shop.ru/catalog/519a8e40b53be1b3/kontrollery-podsvetki/',
        'https://www.dns-shop.ru/catalog/c07ae254c0358d7e/kabeli-razvetviteli-i-udliniteli/',
        'https://www.dns-shop.ru/catalog/2a8f00c7c701409e/derzhateli-dlya-videokart/',
        'https://www.dns-shop.ru/catalog/0e7b09605595ce74/kabel-menedzhment/',
        'https://www.dns-shop.ru/catalog/aa51876b2136bf0a/aksessuary-dlya-ventilyatorov/',
        'https://www.dns-shop.ru/catalog/a1e55b2c4e11cd0b/tovary-dlya-obsluzhivaniya-pk/',
        'https://www.dns-shop.ru/catalog/17a8bbf216404e77/salazki-dlya-nakopitelej/',
        'https://www.dns-shop.ru/catalog/b20c9fc9750b3e70/aksessuary-dlya-korpusa/',
        'https://www.dns-shop.ru/catalog/6f22e17dbcf0a54b/antipylevye-filtry-i-reshetki/',
        'https://www.dns-shop.ru/catalog/17a89c5616404e77/korpusa/',
        'https://www.dns-shop.ru/catalog/17a89c2216404e77/bloki-pitaniya/',
        'https://www.dns-shop.ru/catalog/8a9ddfba20724e77/ssd-nakopiteli/',
        'https://www.dns-shop.ru/catalog/dd58148920724e77/ssd-m2-nakopiteli/',
        'https://www.dns-shop.ru/catalog/ed60465eacbf3c59/adaptery-dlya-nakopitelej/?virtual_category_uid=fcc8496e29ea60cf',
        'https://www.dns-shop.ru/catalog/recipe/4fef73f9c0e09a2c/servernye-ssd/',
        'https://www.dns-shop.ru/catalog/17a9d18916404e77/vneshnie-boksy-dlya-nakopitelej/?virtual_category_uid=ec06a90b485fa7e2',
        'https://www.dns-shop.ru/catalog/17a9d1c016404e77/dok-stancii-dlya-nakopitelej/?virtual_category_uid=0991e87e8e9992ef',
        'https://www.dns-shop.ru/catalog/17a8914916404e77/zhestkie-diski-35/',
        'https://www.dns-shop.ru/catalog/f09d15560cdd4e77/zhestkie-diski-25/',
        'https://www.dns-shop.ru/catalog/17aa4e3216404e77/servernye-hdd/?virtual_category_uid=ab7a4249faa5a46e'
        'https://www.dns-shop.ru/catalog/17a9c97816404e77/opticheskie-privody/',
        'https://www.dns-shop.ru/catalog/17a89b4f16404e77/zvukovye-karty/',
        'https://www.dns-shop.ru/catalog/17a89b8416404e77/karty-videozaxvata/',
        'https://www.dns-shop.ru/catalog/17a89bb916404e77/platy-rasshireniya/',
        'https://www.dns-shop.ru/catalog/ed60465eacbf3c59/adaptery-dlya-nakopitelej/',
        'https://www.dns-shop.ru/catalog/ebc01709b094a079/mnogofunkcionalnye-paneli/',
        'https://www.dns-shop.ru/catalog/recipe/a93cd0f2071b812a/vnesnie-opticeskie-privody/',
    ]

    def __init__(self, name=None, **kwargs):
        super(itemSpider, self).__init__(name, **kwargs)
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(executable_path="/usr/lib/chromium-browser/chromedriver", options=chrome_options)
        self.driver.implicitly_wait(5)

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, method='GET')

    @staticmethod
    def get_selenium_response(driver, url):
        global counter
        driver.get(url)
        time.sleep(3.5)
        if counter == 1:
            try:
                time.sleep(5)
                element = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "city-select__text")))
                time.sleep(0.5)
                element.click()

                element = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, '//span[text()="Приволжский"]')))
                element.click()

                element = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, '//span[text()="Саратовская область"]')))
                element.click()

                element = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, '//span[text()="Саратов"]')))
                element.click()
            except:
                print('Could not change the city!')
            time.sleep(3.5)
        px = 450
        for _ in range(10):
            driver.execute_script(f"window.scrollBy(0,{px});")
            time.sleep(0.5)
        resp = driver.page_source.encode('utf-8')
        return resp

    # Parses the website
    def parse(self, response):
        global counter
        response = Selector(
            text=self.get_selenium_response(self.driver, response.request.url))
        tables = response.xpath(
            "//div[@class='catalog-product ui-button-widget']").getall()
        for row in tables:
            item = DnsItem()
            row_item = Selector(text=row)
            delivery_time = row_item.xpath("//a[@class='delivery-info-widget__button ui-link ui-link_blue']/text()").get()
            available = row_item.xpath(
                "//a[@class='order-avail-wrap__link ui-link ui-link_blue']/span[1]/text()").get()
            if not available:
                available = '0'
            item['available'] = available.strip()
            item['price'] = row_item.xpath(
                "//div[@class='product-buy__price']/text()").get()
            if item['price']:
                item['price'] = item['price'].strip()
            else:
                item['price'] = ''
            item['title'] = ' '.join(row_item.xpath(
                "//a[@class='catalog-product__name ui-link ui-link_black']/span[1]/text()").get().split())
            item['link'] = 'https://www.dns-shop.ru' + row_item.xpath(
                "//a[@class='catalog-product__name ui-link ui-link_black']").attrib['href']
            item['image'] = row_item.xpath(
                "//img[@class='loaded']").attrib['src']
            item['category'] = response.xpath("//h1[@class='title']/text()").get().strip()
            item['sku'] = row_item.xpath('//div').attrib['data-code']
            item['shop'] = 'dns-shop.ru'
            yield item

        counter += 1
        next_page = response.xpath('//a[@class="pagination-widget__page-link pagination-widget__page-link_next "]')

        if next_page:
            next_page_url = f'https://www.dns-shop.ru{next_page.attrib["href"]}&mode=simple'
            yield Request(url=next_page_url, method='GET')

