# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ZhihuPipeline(object):
    def __init__(self):
        self.file = open('zhihu_question.txt', 'w')

    def process_item(self, item, spider):
        line = str(item) + '\n'
        self.file.write(line)

        return item
