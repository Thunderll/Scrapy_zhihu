# -*- coding: utf-8 -*-
from scrapy import Spider
from zhihu.items import ZhihuItem
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
import json

class ZhihuspiderSpider(Spider):
    name = "zhihuSpider"
    allowed_domains = ["zhihu.com"]
    start_urls = ['https://www.zhihu.com']


    def start_requests(self):
        return [Request('https://www.zhihu.com/#signin', meta={'cookiejar': 1}, callback=self.post_login)]

    def post_login(self, response):
        print('Preparging login')
        xsrf = Selector(response).xpath('//input[@name="_xsrf"]/@value').extract()[0]
        print(xsrf)
        return [FormRequest('https://www.zhihu.com/login/email',
                            meta={'cookiejar': response.meta['cookiejar']},
                            formdata={
                                '_xsrf': xsrf,
                                'email': 'your email',
                                'password': 'passwd'},
                            callback=self.after_login,
                            dont_filter=False)]

    def after_login(self, response):
        print('after_login')
        print(json.loads(response.body)['msg'])
        for url in self.start_urls:
            yield Request(url, callback=self.page_parse, dont_filter=True, meta={'cookiejar': response.meta['cookiejar']})

    def page_parse(self, response):
        item = ItemLoader(ZhihuItem(), response)
        item.add_xpath('name','//div[@class="top-nav-profile"]/a/span/text()')
        item.add_xpath('url', '//h2[@class="feed-title"]/a/@href')
        yield item.load_item()
