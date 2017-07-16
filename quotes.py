# -*- coding: utf-8 -*-
import scrapy
from selenium.webdriver.common.by import By
from selenium import webdriver
import time


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['jconline.ne10.uol.com.br/canal/cidades/policia/']
    start_urls = ['http://jconline.ne10.uol.com.br/canal/cidades/policia/']
    driver = webdriver.Chrome(executable_path='/home/kallebe/Downloads/chromedriver')
    driver.get("http://jconline.ne10.uol.com.br/canal/cidades/policia/")

    def parse(self, response):
        urls = response.css('li.lista-noticia-item > a::attr(href)').extract()
        for url in urls:
            url = response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.detalhes_noticia, dont_filter=True)

        self.driver.find_element_by_link_text('Próxima').click()


    def detalhes_noticia(self, response):
        yield {
            'titulo': response.css('h1.titulo-materia::text').extract_first(),
            'sub-titulo' : response.css('p.mg_sutia::text').extract_first(),
            'texto' : response.css('div.t13 manipularFonte.t13.manipularFonte > p::text').extract(),
            'tag': response.css('li.keywords > a::text').extract(),
        }
