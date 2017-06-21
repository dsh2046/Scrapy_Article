# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
import re

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

        next_urls = response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_urls:
            yield Request(url=parse.urljoin(response.url, next_urls), callback=self.parse)

    def parse_detail(self, response):
        article_item = JobBoleArticleItem()

        front_image_url = response.meta.get("front_image_url", "")  # Title images url
        title = response.xpath("//div[@class='entry-header']/h1/text()").extract()[0]
        create_date = response.xpath("//p[@class='entry-meta-hide-on-mobile']/text()[1]").extract()[0].strip().replace('·', '').strip()
        praise_nums = int(response.xpath("//div[@class='post-adds']/span/h10/text()").extract()[0])
        fav_nums = int(re.findall(r'(\d+)', response.xpath("//div[@class='post-adds']/span[2]/text()").extract()[0])[0])
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
        article_item['create_date'] = create_date
        article_item['front_image_url'] = [front_image_url]
        article_item['praise_nums'] = praise_nums
        article_item['fav_nums'] = fav_nums
        article_item['comment_nums'] = comment_nums
        article_item['tags'] = tags
        article_item['content'] = content

        yield article_item
