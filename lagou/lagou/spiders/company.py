# -*- coding: utf-8 -*-
from lagou.items import LagouItem
import scrapy


class CompanySpider(scrapy.Spider):
	name = 'company'
	# allowed_domains = ['lagou.com/']
	# cookie = {
 #        "JSESSIONID": "ABAAABAAAGGABCB090F51A04758BF627C5C4146A091E618",
 #        "_ga": "GA1.2.1916147411.1516780498",
 #        "_gid": "GA1.2.405028378.1516780498",
 #        "Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6": "1516780498",
 #        "user_trace_token": "20180124155458-df9f65bb-00db-11e8-88b4-525400f775ce",
 #        "LGUID": "20180124155458-df9f6ba5-00db-11e8-88b4-525400f775ce",
 #        "X_HTTP_TOKEN": "98a7e947b9cfd07b7373a2d849b3789c",
 #        "index_location_city": "%E5%85%A8%E5%9B%BD",
 #        "TG-TRACK-CODE": "index_navigation",
 #        "LGSID": "20180124175810-15b62bef-00ed-11e8-8e1a-525400f775ce",
 #        "PRE_UTM": "",
 #        "PRE_HOST": "",
 #        "PRE_SITE": "https%3A%2F%2Fwww.lagou.com%2F",
 #        "PRE_LAND": "https%3A%2F%2Fwww.lagou.com%2Fzhaopin%2FJava%2F%3FlabelWords%3Dlabel",
 #        "_gat": "1",
 #        "SEARCH_ID": "27bbda4b75b04ff6bbb01d84b48d76c8",
 #        "Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6": "1516788742",
 #        "LGRID": "20180124181222-1160a244-00ef-11e8-a947-5254005c3644"
 #    }
	headers = {
    'Connection': 'keep - alive',  # 保持链接状态
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36',
    'Cookie': 'JSESSIONID=ABAAABAABEEAAJA0EE5754B8F40B4BAF4E709998F59A5F7; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1545794665; _ga=GA1.2.495570545.1545794665; user_trace_token=20181226112512-daf665e1-08bd-11e9-ad84-5254005c3644; LGUID=20181226112512-daf66913-08bd-11e9-ad84-5254005c3644; index_location_city=%E5%8C%97%E4%BA%AC; X_HTTP_TOKEN=e6ec0dbc8c136917d9598606f4f4793b; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22167e99d3fef330-0668e5a483149a-2711639-1440000-167e99d3ff034e%22%2C%22%24device_id%22%3A%22167e99d3fef330-0668e5a483149a-2711639-1440000-167e99d3ff034e%22%7D; TG-TRACK-CODE=index_navigation; _gid=GA1.2.1274730007.1545903467; LGSID=20181227173833-2d636672-09bb-11e9-ad84-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Fgongsi%2F2-1-33-1; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fgongsi%2F45361.html; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1545903701; LGRID=20181227174227-b8e3f6ee-09bb-11e9-b128-525400f775ce'
    }
	start_urls = ['http://lagou.com/gongsi/']
	def parse(self, response):
		item = LagouItem()
		tag_url = response.xpath('//li[@class="wrapper"]//div/ul/li/a/@href')
		next_page = response.xpath('//div[@class="pager_container"]/span[last()]/@class')
		for each in response.xpath('//li[@class="company-item"]'):
			lg_company_url = each.xpath('div/p[1]/a/@href').extract_first()
			tag = each.xpath('div/p[@class="indus-stage wordCut"]/text()').extract_first()
			item['tag'] = tag
			item['lg_company_url'] = lg_company_url
			# for i in range(1,21):


			#print(item,next_page)
		# for url in tag_url:
		# 	yield scrapy.Request(next_page, callback=self.parse)
			# print(lg_company_url)
		yield scrapy.Request(url='https://www.lagou.com/gongsi/10483.html',headers=self.headers,callback=self.company_page,meta={'item':item})
	def company_page(self,response):
		print('开始回调')
		#item = LagouItem()
		item = response.meta['item']
		company_url = response.xpath('//h1/a/@href').extract_first()
		img_log = response.xpath('//div[@class="top_info_wrap"]/img/@src').extract_first()
		company_word = response.xpath('//div[@class="company_word"]/text()').extract_first().strip()
		item['company_url'] = company_url
		item['company_word'] = company_word
		item['img_log'] = img_log
		yield item