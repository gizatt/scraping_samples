# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from recipes.items import RecipesItem


class AllrecipesSpider(CrawlSpider):
    name = 'allrecipes'
    allowed_domains = ['allrecipes.com']
    start_urls = ['http://www.allrecipes.com/']

    rules = (   
        Rule(LinkExtractor(allow=(r'/Recipe/', r'/recipe/'), deny=(r'\?sitepref\=m')), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        i = RecipesItem()
        i['name'] = response.xpath('//h1[@id="itemTitle"]/text()').extract_first()
        i['author'] = response.xpath('//*[@id="lblSubmitter"]/a/text()').extract_first()
        i['servings'] = response.xpath('//*[@id="lblYield"]/text()').re_first(r'(.*) servings')
        
        columns = response.xpath('//ul[contains(@class,"ingredient-wrap")]')
        ingredients_all = {}
        for column in columns:
            ingredients = column.xpath('./li[@id="liIngredient"]')
            for ingredient in ingredients:
                ingredients_all[ingredient.xpath('.//span[@id="lblIngName"]/text()').extract_first()] = \
                    ingredient.xpath('.//span[@id="lblIngAmount"]/text()').extract_first()

        i['ingredients'] = ingredients_all

        directions = response.xpath('//div[@class="directions"]//li/span')
        directions_all = {}
        for index, direction in enumerate(directions):
            directions_all[index] = direction.xpath('./text()').extract_first()

        i['directions'] = directions_all
        i['rating'] = response.xpath('(//*[@itemProp="ratingValue"]/@content)[1]').extract_first()
        i['principal_image'] = response.xpath('//*[@id="imgPhoto"]/@src').extract_first()
        i['url'] = response.url

        return i
