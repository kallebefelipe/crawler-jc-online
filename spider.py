# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import re
import json
import unicodedata
import re


def normalize_ascii(value):
    return unicodedata.normalize('NFKD', value) \
        .encode('ascii', 'ignore')


def normalize_string(value):
    return str(normalize_ascii(value))[2:-1].strip()


dados = []
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
        i = 0
        while True:
            i += 1
            self.driver.find_element_by_link_text('Próxima').click()
            self.parse(HtmlResponse(self.driver.page_source))
            response =  HtmlResponse(self.driver.current_url, body=self.driver.page_source, encoding='utf-8')
            urls = response.css('li.lista-noticia-item > a::attr(href)').extract()
            for url in urls:
                url = response.urljoin(url)
                yield scrapy.Request(url=url, callback=self.detalhes_noticia, dont_filter=True)
            print(i)
            time.sleep(3)
            if i > 500:
                break
        self.escrever_dados()

    def detalhes_noticia(self, response):
        noticia ={
            'titulo': response.css('h1.titulo-materia::text').extract_first().lower(),
            'sub-titulo': response.css('p.mg_sutia::text').extract_first().lower(),
            'texto': response.css('div.t13.manipularFonte > p::text').extract(),
            'tag': response.css('li.keywords > a::text').extract(),
            'data': response.css('p.data-materia::text').extract_first(),
        }
        self.carregar_noticia(noticia)
        yield noticia

    def tratar_texto(self, textos):
        texto = ''
        for tex in textos:
            texto += ' '+tex.lower()
        return texto

    def tratar_data(self, texto):
        data = re.search(r'[0-9][0-9]/[0-9][0-9]/[0-9][0-9][0-9][0-9]', texto).group()
        return data

    def tratar_hora(self, texto):
        hora = re.search(r'[0-9][0-9]h[0-9][0-9]', texto).group()
        hora = hora.split('h')
        hora = hora[0]+':'+hora[1]
        return hora

    def carregar_noticia(self, noticia):
        noticia['texto'] = normalize_string(self.tratar_texto(noticia['texto']))
        noticia['tag'] = normalize_string(self.tratar_texto(noticia['tag']))
        noticia['hora'] = normalize_string(self.tratar_hora(noticia['data']))
        noticia['data'] = normalize_string(self.tratar_data(noticia['data']))
        noticia['titulo'] = normalize_string(noticia['titulo'])
        noticia['sub-titulo'] = normalize_string(noticia['sub-titulo'])
        dados.append(noticia)

    def escrever_dados(self):
        with open('data.txt', 'w') as outfile:
            json.dump(dados, outfile)

# from scrapy.http import HtmlResponse
# from selenium import webdriver

# class JSMiddleware(object):
#     def process_request(self, request, spider):
#         driver = webdriver.PhantomJS()
#         driver.get(request.url)

#         body = driver.page_source
#         return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)
