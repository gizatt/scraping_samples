# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RecipesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    author = scrapy.Field()
    servings = scrapy.Field()
    ingredients = scrapy.Field()
    directions = scrapy.Field()
    rating = scrapy.Field()
    ratings = scrapy.Field()
    url = scrapy.Field()
