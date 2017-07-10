# -*- coding: utf-8 -*-
import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['jconline.ne10.uol.com.br/canal/cidades/policia/']
    start_urls = ['http://jconline.ne10.uol.com.br/canal/cidades/policia/']

    def parse(self, response):
        for quote in response.css('ul.box-lista-noticias'):
            yield {
                # 'titulo' : response.css('h1.bloco_titulo.esq::text').extract_first(),
                'noticia' : response.css('a::text').extract()
            }
