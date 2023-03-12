import time

from scrapy import *
from onlinetrade.items import OnlinetradeItem
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth

class SiteSpider(Spider):
    name = 'OnlineTradeSpider'

    BASE_URL = 'https://www.onlinetrade.ru'
    QUERY = '?per_page=45&c=61&browse_mode=4'
    SHOP = 'onlinetrade.ru'

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Referer": "https://www.onlinetrade.ru",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        "sec-ch-ua": "\".Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"103\", \"Chromium\";v=\"103\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }

    cookies = {
        "user_city": "61",
        "user_c": "61",
        "items_per_page": "45",
        "browse_mode": "2",
        "_ym_isad": "1"
    }

    def __init__(self, name=None, **kwargs):
        super(SiteSpider, self).__init__(name, **kwargs)
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(executable_path=r"C:\Users\Adam\Downloads\chromedriver_win32\chromedriver.exe", options=chrome_options)

        stealth(self.driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )

        self.driver.implicitly_wait(5)


    def start_requests(self):
        urls = [
            'https://www.onlinetrade.ru/catalogue/videokarty-c338/',
            'https://www.onlinetrade.ru/catalogue/materinskie_platy-c340/',
            'https://www.onlinetrade.ru/catalogue/protsessory-c342/',
            'https://www.onlinetrade.ru/catalogue/operativnaya_pamyat-c341/',
            'https://www.onlinetrade.ru/catalogue/bloki_pitaniya-c339/',
            'https://www.onlinetrade.ru/catalogue/ssd_diski-c294/',
            'https://www.onlinetrade.ru/catalogue/zhestkie_diski_hdd-c174/',
            'https://www.onlinetrade.ru/catalogue/zvukovye_karty-c1482/',
            'https://www.onlinetrade.ru/catalogue/kompyuternye_korpusa-c1323/',
            'https://www.onlinetrade.ru/catalogue/kulery_dlya_protsessorov-c1492/',
            'https://www.onlinetrade.ru/catalogue/sistemy_vodyanogo_okhlazhdeniya_pk-c4941/',
            'https://www.onlinetrade.ru/catalogue/ventilyatory_dlya_korpusa-c1322/',
            'https://www.onlinetrade.ru/catalogue/kulery_dlya_videokart-c1603/',
            'https://www.onlinetrade.ru/catalogue/termopasty-c1327/',
            'https://www.onlinetrade.ru/catalogue/termoprokladki-c7568/',
            'https://www.onlinetrade.ru/catalogue/kabeli_shleyfy_i_perekhodniki-c712/',
            'https://www.onlinetrade.ru/catalogue/opticheskie_privody-c172/',
            'https://www.onlinetrade.ru/catalogue/konteynery_adaptery_perekhodniki_dlya_hdd_ssd-c1328/',
            'https://www.onlinetrade.ru/catalogue/tv_tyunery_i_videomontazh-c3940/',
            'https://www.onlinetrade.ru/catalogue/aksessuary_dlya_svo-c4040/',
            'https://www.onlinetrade.ru/catalogue/aksessuary_dlya_moddinga_pk-c3952/',
            'https://www.onlinetrade.ru/catalogue/aksessuary_dlya_korpusa-c5882/',
            'https://www.onlinetrade.ru/catalogue/komponenty_dlya_mac-c6248/',
            'https://www.onlinetrade.ru/catalogue/kabeli_apple-c6942/'
        ]

        for url in urls:
            yield Request(url=f'{url}{self.QUERY}0', cookies=self.cookies, headers=self.headers, callback=self.parse, dont_filter = True)

    @staticmethod
    def get_selenium_response(driver, url):
        driver.get(url)
        time.sleep(2)
        resp = driver.page_source.encode('utf-8')
        return resp

    def parse(self, response):

        response = Selector(
            text=self.get_selenium_response(self.driver, response.request.url))
        table = response.xpath("//div[@class='indexGoods__item']").getall()

        for rows in table:
            row = Selector(text=rows)
            item = OnlinetradeItem()
            try:
                item['link'] = self.BASE_URL + row.xpath("//a[@class='indexGoods__item__name  indexGoods__item__name__3lines  ']/@href").get()
                item['title'] = row.xpath("//a[@class='indexGoods__item__name  indexGoods__item__name__3lines  ']/text()").get().strip()
            except Exception:
                item['link'] = self.BASE_URL + row.xpath("//a[@class='indexGoods__item__name  ']/@href").get()
                item['title'] = row.xpath("//a[@class='indexGoods__item__name  ']/text()").get().strip()

            try:
                item['price'] = row.xpath("//span[@class='price regular js__actualPrice']/text()").get().strip()
            except AttributeError:
                item['price'] = row.xpath("//span[@class='price js__actualPrice']/text()").get().strip()
            item['price'] = item['price'].replace('₽', '')
            item['price'] = item['price'].replace(' ', '')
            item['available'] = row.xpath("//span[@class='catalog__displayedItem__availabilityCount']/text()").get()
            if item['available']:
                item['available'] = item['available'].strip()
                erase = ['в наличии ', '> ', ' шт.']
                for s in erase:
                    item['available'] = item['available'].replace(s, '')
            else:
                item['available'] = '0'

            try:
                item['image'] = row.xpath("//img/@src").get()
            except TypeError:
                item['image'] = ''

            item['shop'] = self.SHOP
            item['sku'] = row.xpath("//div[@class='indexGoods__item__storeCode']/text()").get().strip()
            item['category'] = response.xpath("//h1/text()").get().split(' -')[0]

            yield item

        next_page = response.xpath("//a[text()='→']/@href")

        if next_page:
            next_page_url = self.BASE_URL + next_page.get()
            yield Request(url=next_page_url, cookies=self.cookies, headers=self.headers, callback=self.parse, dont_filter = True)