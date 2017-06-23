# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import datetime
import re
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join


# class ArticlespiderItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass
#
def date_convert(value):
    try:
        create_date = datetime.datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        create_date = datetime.datetime.now().date()
    return create_date


def get_nums(value):
    try:
        nums = int(re.findall(r'(\d+)', value)[0])
    except IndexError:
        nums = 0

    return nums


def tags_filter(value):
    if "评论" not in value:
        print(value)
        return value


# 自定义默认itemloader, 默认输出取数组的第一个值, 输出为字符串而不是数组
class ArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class JobBoleArticleItem(scrapy.Item):
    title = scrapy.Field()
    create_date = scrapy.Field(
        input_processor=MapCompose(date_convert),
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    front_image_url = scrapy.Field(
        output_processor=MapCompose(lambda x: x)
    )
    front_image_path = scrapy.Field()
    praise_nums = scrapy.Field(input_processor=MapCompose(get_nums))
    comment_nums = scrapy.Field(input_processor=MapCompose(get_nums))
    fav_nums = scrapy.Field(input_processor=MapCompose(get_nums))
    tags = scrapy.Field(
        input_processor=MapCompose(tags_filter),
        output_processor=Join(",")
    )
    content = scrapy.Field()

