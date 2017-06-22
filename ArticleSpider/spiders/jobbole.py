# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.loader import ItemLoader
from urllib import parse
import re
import datetime

from ArticleSpider.items import JobBoleArticleItem

from ArticleSpider.utils.common import get_md5


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        post_nodes = response.css("div#archive .floated-thumb .post-thumb a")
        for post_node in post_nodes:
            image_url = post_node.css("img::attr(src)").extract_first("")
            post_url = post_node.css("::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": image_url}, callback=self.parse_detail)

        # next_urls = response.css(".next.page-numbers::attr(href)").extract_first("")
        # if next_urls:
        #     yield Request(url=parse.urljoin(response.url, next_urls), callback=self.parse)

    def parse_detail(self, response):
        article_item = JobBoleArticleItem()

        front_image_url = response.meta.get("front_image_url", "")  # Title images url
        title = response.xpath("//div[@class='entry-header']/h1/text()").extract()[0]
        create_date = response.xpath("//p[@class='entry-meta-hide-on-mobile']/text()[1]").extract()[0].strip().replace('·', '').strip()
        try:
            praise_nums = int(response.xpath("//div[@class='post-adds']/span/h10/text()").extract()[0])
        except IndexError:
            praise_nums = 0
        try:
            fav_nums = int(re.findall(r'(\d+)', response.xpath("//div[@class='post-adds']/span[2]/text()").extract()[0])[0])
        except IndexError:
            fav_nums = 0
        try:
            comment_nums = int(re.findall(r'(\d+)', response.xpath("//div[@class='post-adds']/a/span/text()").extract()[0])[0])
        except IndexError:
            comment_nums = 0
        tag_list = list(set(response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()))
        tags = ','.join(tag_list)
        content = response.xpath("//div[@class='entry']").extract()[0]

        article_item['url_object_id'] = get_md5(response.url)
        article_item['title'] = title
        article_item['url'] = response.url
        try:
            create_date = datetime.datetime.strptime(create_date, "%Y/%m/%d").date()
        except Exception as e:
            create_date = datetime.datetime.now().date()
        article_item['create_date'] = create_date
        article_item['front_image_url'] = [front_image_url]
        article_item['praise_nums'] = praise_nums
        article_item['fav_nums'] = fav_nums
        article_item['comment_nums'] = comment_nums
        article_item['tags'] = tags
        article_item['content'] = content

        # 通过itemloader加载item
        item_loader = ItemLoader(item=JobBoleArticleItem(), response=response)
        item_loader.add_css()
        item_loader.add_xpath("title", "//div[@class='entry-header']/h1/text()")
        item_loader.add_xpath("create_date", "//p[@class='entry-meta-hide-on-mobile']/text()[1]")
        item_loader.add_xpath("praise_nums", "//div[@class='post-adds']/span/h10/text()")
        item_loader.add_xpath("fav_nums", "//div[@class='post-adds']/span[2]/text()")
        item_loader.add_value()


        yield article_item
