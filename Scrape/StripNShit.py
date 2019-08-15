from bs4 import BeautifulSoup
import requests
from selenium import webdriver

# 'https://www.google.com/search?q=' + q + '&ie=utf-8&oe=utf-8'
# q is the search itself
# <g-inner-card class="cv2VAd">

class StripNShit:
    def __init__(self, ticker):
        self.raw_news = []
        self.ticker = ticker
        self.update()

    def update(self):
        chrome_path = "C:/chromedriver"
        driver = webdriver.Chrome(executable_path=chrome_path)
        driver.get('https://www.google.com/search?q=' + self.ticker + '&ie=utf-8&oe=utf-8')
        g = driver.find_elements_by_class_name('cv2VAd')

        news_links = []
        _count = 0
        for x in g:
            if _count > 9:
                break

            news_links.append(x.find_element_by_xpath('.//a').get_attribute('href'))
            _count += 1

        driver.close()

        self.raw_news = []
        for link in news_links:
            _html = requests.get(link).text
            html = BeautifulSoup(_html, 'lxml')
            self.raw_news.append(html.get_text())

