# -*- coding: utf-8 -*-
import scrapy
import re
import json


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36"
    header = {
        "HOST": "www.zhihu.com",
        "Referer": "https://www.zhihu.com",
        "User-Agent": agent
    }

    def parse(self, response):
        pass

    def parse_detail(self):
        pass

    def start_requests(self):
        return [scrapy.Request('https://www.zhihu.com/#signin', headers=self.header, callback=self.login)]

    def login(self, response):
        response_text = response.text
        match_obj = re.match('.*name="_xsrf" value="(.*?)"', response_text, re.DOTALL)
        xsrf = ''
        if match_obj:
            xsrf = (match_obj.group(1))

        if xsrf:
            post_url = "https://www.zhihu.com/login/phone_num"
            post_data = {
                "_xsrf": xsrf,
                "phone_num": "6472159987",
                "password": "dsh20462046",
            }

            return [scrapy.FormRequest(
                url=post_url,
                formdata=post_data,
                headers=self.header,
                callback=self.check_login
            )]

    def check_login(self, response):
        text_json = json.loads(response.text)
        if 'msg' in text_json and text_json['msg'] == '登录成功':
            for url in self.start_urls:
                yield scrapy.Request(url, dont_filter=True, headers=self.header)
        pass






