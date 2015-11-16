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
        i['name'] = response.xpath('//h1[@class="recipe-summary__h1"]/text()').extract_first()
        i['author'] = response.xpath('//span[@class="submitter__name"]/text()').extract_first()
        i['servings'] = int(response.xpath('//meta[@itemprop="recipeYield"]/@content').extract_first())
        
        columns = response.xpath('//ul[contains(@id, "lst_ingredients")]')
        ingredients_all = []
        for column in columns:
            ingredients = column.xpath('./li[@class="checkList__line"]')
            for ingredient in ingredients:
                ingred = ingredient.xpath('.//span[@itemprop="ingredients" and contains(@class, "recipe-ingred_txt")]/text()').extract_first()
                if ingred:
                    ingredients_all.append(ingred)

        i['ingredients'] = ingredients_all

        directions = response.xpath('//ol[@class="list-numbers recipe-directions__list"]//li/span')
        directions_all = {}
        for index, direction in enumerate(directions):
            directions_all[index] = direction.xpath('./text()').extract_first()

        i['directions'] = directions_all
        i['rating'] = float(response.xpath('//div[contains(@class,"rating-stars")]/@data-ratingstars').extract_first())

        i['ratings'] = int(response.xpath('//span[@class="review-count"]/text()').extract_first())

        i['url'] = response.url

        return i
