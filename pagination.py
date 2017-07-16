import scrapy
from selenium import webdriver


class northshoreSpider(scrapy.Spider):
    name = 'xxx'
    allowed_domains = ['jconline.ne10.uol.com.br/canal/cidades/policia/']
    start_urls = ['http://jconline.ne10.uol.com.br/canal/cidades/policia/']

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path='/home/kallebe/Downloads/chromedriver')

    def parse(self, response):
            self.driver.get('http://jconline.ne10.uol.com.br/canal/cidades/policia/')

            while True:
                try:
                    next = self.driver.find_element_by_link_text('Próxima')
                    url = 'http://jconline.ne10.uol.com.br/canal/cidades/policia/'
                    yield scrapy.Request(url, callback=self.parse2)
                    next.click()
                except:
                    break

            self.driver.close()

    def parse2(self, response):
        import ipdb; ipdb.set_trace()
        print('you are here!')
