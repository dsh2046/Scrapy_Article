# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
import re


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        post_urls = response.css("a.archive-title::attr(href)").extract()
        for post_url in post_urls:
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse_detail)
        next_urls = response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_urls:
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse)

    def parse_detail(self, response):
        title = response.xpath("//div[@class='entry-header']/h1/text()").extract()[0].extract()[0]
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



        pass
