# -*- coding: utf-8 -*-
import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['jconline.ne10.uol.com.br/canal/cidades/policia/']
    start_urls = ['http://jconline.ne10.uol.com.br/canal/cidades/policia/']

    def parse(self, response):
        urls = response.css('li.lista-noticia-item > a::attr(href)').extract()
        for url in urls:
            url = response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.detalhes_noticia)

        next_page_url = response.css('li.next > a::attr(href)').extract_first()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def detalhes_noticia(self, response):
        print(response.text)
        yield {
            'titulo': response.css('h1.titulo-materia::text').extract_first(),
            # 'bairro': response.css('div.mg_chapeu::text').extract_first(),
            # 'texto': response.css('div.noticia_corponoticia > p::text').extract_first(),
            # 'tag': response.css('div.mg_chapeu::text').extract_first(),
        }
