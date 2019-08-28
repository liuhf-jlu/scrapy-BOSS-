# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from BJ.items import BjItem
import time

class BossZhipinSpider(scrapy.Spider):
    name = 'boss_zhipin'   # 运行时爬虫的名称
    allowed_domains = ['zhipin.com']  # 当 OffsiteMiddleware 启用时， 域名不在列表中的URL不会被跟进。
    start_urls = ['https://www.zhipin.com/c101010100/?query=python&page=1&ka=page-1']  # 起始url

    cookie_list="lastCity=101010100; _uab_collina=156690786993771845122604; __zp_stoken__=91d9sehzkp8EbGAr%2FhorhnBlKDxF48iLYCkIFKXQWc%2BBsP9gUqC13U399dM5YAVVefystK0H6%2BtLx651FN%2BybujeYw%3D%3D; __c=1566962162; __g=-; __l=l=%2Fwww.zhipin.com%2Fjob_detail%2F%3Fquery%3Dpython%26city%3D101010100%26industry%3D%26position%3D&r=; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1566907870,1566962162; __a=85199832.1566370536.1566907870.1566962162.21.3.14.21; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1566973807"

    custom_settings = {
        "COOKIES_ENABLED": False,
        "DOWNLOAD_DELAY": 1,
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Cookie': cookie_list,
            'Host': 'www.zhipin.com',
            'Origin': 'https://www.zhipin.com',
            'Referer': 'https://www.zhipin.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
        }
    }


    def parse(self, response):
        item =BjItem()
        # 获取页面数据的条数
        nodeList = response.xpath('//div[@class="job-primary"]')
        for node in nodeList:
            item["job_title"]=node.xpath('.//div[@class="job-title"]/text()').extract()[0]
            item["compensation"]=node.xpath('.//span[@class="red"]/text()').extract()[0]
            item["company"]=node.xpath('.//div[@class="info-company"]//h3//a/text()').extract()[0]
            company_info=node.xpath('.//div[@class="info-company"]//p/text()').extract()
            temp=node.xpath('.//div[@class="info-primary"]//p/text()').extract()
            item["address"] = temp[0]
            item["seniority"] = temp[1]
            item["education"] = temp[2]
            if len(company_info) < 3:
                item["company_type"] = company_info[0]
                item["company_finance"] = ""
                item["company_quorum"] = company_info[-1]
            else:
                item["company_type"] = company_info[0]
                item["company_finance"] = company_info[1]
                item["company_quorum"] = company_info[2]
            yield item
        next_page=response.xpath('//div[@class="page"]//a[@class="next"]/@href').extract()[-1]
        if next_page != "javascript:;":
            base_url="https://www.zhipin.com"
            url=base_url+next_page
            time.sleep(5)  # 设置爬取延迟
            yield Request(url=url,callback=self.parse)