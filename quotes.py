# -*- coding: utf-8 -*-
import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['http://jconline.ne10.uol.com.br/canal/cidades/policia/']
    start_urls = ['http://http://jconline.ne10.uol.com.br/canal/cidades/policia//']

    def parse(self, response):
        pass
