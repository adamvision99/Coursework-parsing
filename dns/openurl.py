import urllib3
import requests
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


class SeleniumBrowser(object):
    options = None
    browser = None

    def __init__(self):
        options = Options()
        DRIVER_PATH = 'C:/Users/Armen/Downloads/geckodriver.exe'

        # set headleess | invisble mode
        options.add_argument("--headless")

        self.browser = webdriver.Firefox(executable_path=DRIVER_PATH,
                                         options=options)
        self.browser.maximize_window()
        # self.browser = webdriver.Firefox(executable_path = 'geckodriver.exe', options=options)

    def get(self, url):
        self.browser.get(url)
        time.sleep(12)
        try:
            self.browser.find_element("xpath", "//p[@class='city-select__text']").click()
            time.sleep(5)
            self.browser.find_element('xpath', '//span[text()="Приволжский"]').click()
            self.browser.find_element('xpath', '//span[text()="Саратовская область"]').click()
            self.browser.find_element('xpath', '//span[text()="Саратов"]').click()
        except:
            print('Could not change the city!')
        time.sleep(5)
        px = 450
        for _ in range(10):
            self.browser.execute_script(f"window.scrollBy(0,{px});")
            time.sleep(0.6)
        source = self.browser.page_source
        self.browser.quit()
        return source

