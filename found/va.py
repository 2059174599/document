from fake_useragent import UserAgent
from lxml import etree
import traceback
import pymysql
import requests
import aiohttp
import asyncio
import time
import re

sem = asyncio.Semaphore(10) # 信号量，控制协程数，防止爬的过快

def get_post_html(url):
	#ua = UserAgent()
	for i in range(2): # 页码
		data = { 
		#'selRTE': ,
		'sr_pagehit': 25, # 每页显示量
		'sr_pagetogo': i+1,
		'sr_pagetogoBottom': i,
		#'api_applids': ,
		'sr_orderby': 'default',
		'sr_order': 'ASC',
		'sr_startrow': 1+25*i,
		'sr_pagenum': i+1,
		'sr_maxpagenum': 3444,
		'sr_qsval': 45135626,
		#'ddparam': ,
		#'ddvalue': ,
		# 'ddsub': ,
		# 'hdnSelProjects': ,
		'hdnPagingtxt': 1,
		#'pball': ,
		'hICDE': 45135626,
		#'hsq': 
		}
		headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '247',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'REPORTERPORTFOLIO=""; RUPSID=33580616; Exist; _ga=GA1.2.1667170292.1560761802; _gid=GA1.2.1493207448.1560761802; _ga=GA1.3.1667170292.1560761802; _gid=GA1.3.1493207448.1560761802; LIKEAID=""; REPORTERLF=""; JSESSIONID=08CDCFB32C9A6E442F331F1FC7E51742.RePORTER; CFID=2784793; CFTOKEN=69015824; _gat=1; _gat_RePORTER=1; _gat_GSA_ENOR0=1; REPORTERPAGING=sr%5Forderby%3Ddefault%7Csr%5Forder%3DASC%7Csr%5Fpagehit%3D25%7Csr%5Fstartrow%3D51%7Csr%5Fpagenum%3D3',
        'Host': 'projectreporter.nih.gov',
        'Origin': 'https://projectreporter.nih.gov',
        'Referer': 'https://projectreporter.nih.gov/reporter_SearchResults.cfm?icde=45135626',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
		}
		r = requests.post(url,headers=headers,data = data,timeout = 20)
		time.sleep(3)
		# with open('va.html', 'w') as f:
		# 	f.write(r.text)
		print('开始采集前'+ str((i+1)*25) + '个')
		yield r.text
	
def get_html(url):
	ua = UserAgent()
	headers = {
	#'User-Agent':ua.random
	'User-Agent':'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:21.0.0) Gecko/20121011 Firefox/21.0.0',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	'Cookie': 'REPORTERPORTFOLIO=""; RUPSID=33580616; Exist; _ga=GA1.2.1667170292.1560761802; _gid=GA1.2.1493207448.1560761802; _ga=GA1.3.1667170292.1560761802; _gid=GA1.3.1493207448.1560761802; LIKEAID=""; REPORTERLF=""; REPORTERPAGING=sr%5Forderby%3Ddefault%7Csr%5Forder%3DASC%7Csr%5Fpagehit%3D25%7Csr%5Fstartrow%3D26%7Csr%5Fpagenum%3D2; JSESSIONID=B824E75D48DBF5054C9F9C67342B697E.RePORTER; CFID=2671667; CFTOKEN=77314224'
	}
	r = requests.get(url,headers=headers,timeout = 10)
	return r.text
# 页码
def get_page(html):
	cont = etree.HTML(html)
	h1 = cont.xpath('//p[@class="pageTotal"]/span/text()')[0]
	return h1
# async def get_html(url):
	# with(await sem):
		# # async with是异步上下文管理器
		# async with aiohttp.ClientSession() as session:  # 获取session
			# async with session.get(url,timeout = 10) as r:  # 提出请求
				# #return r.text
				# print(url.split('-')[-1])
				# text = await r.text()
				# get_snsf_content(text,url)

def get_found_url(html):
	cont = etree.HTML(html)
	# for urls in cont.xpath('//table[@class="proj_search_cont"]/tbody/tr/td[3]/a/@href'):
		# url = urls.xpath('td[3]/a/@href')
		# yield url
	# urls  = cont.xpath('//table[@class="proj_search_cont"]/tbody/tr')
	# test = re.findall('<td width="8px">(.*?)\'',html,re.S)
	for urls in cont.xpath('//table[@class="proj_search_cont"]/tbody/tr'):
		host = 'https://projectreporter.nih.gov/'
		href = urls.xpath('td[4]/a/@href')
		if href:
			url = host + href[0]
			yield url
def get_frqnt_content(Html,url):
	item = {}
	html = etree.HTML(Html)
	item['title'] = html.xpath('//h1[@class="sectionTitle mainTitle"]/text()')[0].strip() # 标题
	item['lead'] = html.xpath('//h3/text()')[0].strip() # 项目负责人
	item['accept_subsidize_institution'] = html.xpath('//h4/text()')[0].strip() # 受资助机构
	time = html.xpath('//div[@class="wysiwyg_container"]/p[5]/strong/text()')[0].strip()
	item['apply_years'] = re.search('Concours(.*?)-',time,re.S).group(1).strip() #申请年份
	item['plan_time'] = item['apply_years'] + '-01-01' # 计划开始时间
	item['domain_classifica'] = html.xpath('//div[@class="wysiwyg_container"]/p[3]/strong/text()')[0].replace('Domaine :','').strip() # 领域分类
	item['summary'] = html.xpath('string(//div[@id="fragment-1"]/div)').strip() # 摘要
	item['project_type'] = 'team research project' # 项目类别
	item['subsidize_institution'] = 'FRQNT' # 资助机构
	item['project_lavel'] = 'Provincial' # 项目级别
	item['subsidize_country'] = 'CANADA' # 资助国家
	item['url'] = url
	# print(item)
		#write_item(item)
	sql = """INSERT INTO found_frqnt (title,lead,accept_subsidize_institution,apply_years,plan_time,domain_classifica,summary,project_type,subsidize_institution,project_lavel,subsidize_country,url) \
		values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')""" % \
		(pymysql.escape_string(item['title']), item['lead'], item['accept_subsidize_institution'], item['apply_years'], pymysql.escape_string(item['plan_time']), pymysql.escape_string(item['domain_classifica']), pymysql.escape_string(item['summary']), pymysql.escape_string(item['project_type']), pymysql.escape_string(item['subsidize_institution']), item['project_lavel'], item['subsidize_country'], item['url'])#sql
		# ##(item['标题'], item['计划开始时间'], item['计划结束时间'], item['申请年份'], item['项目类别'], item['领域分类'], item['受资助机构'], item['项目负责人'], item['关键词'], item['资助机构'], item['资助国家'], item['摘要'], item['资助金额'], item['url'])
	db_execute(sql) #入库

#保存
def write_item(item):
	path = r'frqnt_error.txt'
	with open(path,'a+',encoding='utf-8') as f:
		f.write(str(item) + '\n')

#链接数据库
def db_execute(sql):
    dbs = pymysql.connect(
                            host='192.168.200.102',
                            user='wxy', 
                            passwd='66357070', 
                            db='cn_web',
                            port=3306,
                            charset="utf8"
                        )
    cursor = dbs.cursor()
    #print('链接数据库')
    try:
        dbs.autocommit(True)
        cursor.execute(sql)
        dbs.commit()
    except:
        traceback.print_exc() #异常处理
        dbs.rollback() #回滚
    cursor.close()
	
def main():
	url = 'https://projectreporter.nih.gov/reporter_SearchResults.cfm?icde=45135626'
	for page_content in get_post_html(url):
		urls = get_found_url(page_content) # 内容页url
		for page_url in urls:
			print(page_url)
			# cont = get_html(page_url)
			# get_frqnt_content(cont,page_url)
	# start_url = 'http://www.frqnt.gouv.qc.ca/en/la-recherche/la-recherche-financee-par-le-frqnt/projets-de-recherche?field=0&researcher_name=&year=0&institution=0&program=0&submit=%E6%90%9C%E7%B4%A2'
	# page_content = get_html(start_url)
	# page_num = get_page(page_content)
	# for i in range(1,int(page_num)+1):
		# url1 = 'http://www.frqnt.gouv.qc.ca/en/la-recherche/la-recherche-financee-par-le-frqnt/projets-de-recherche?page='
		# url2 = '&field=0&institution=0&program=0&year=0&sort=year-desc'
		# url = url1 + str(i) +url2
		# cont_html = get_html(url)
		# found_urls = get_found_url(cont_html)
		# for found_url in found_urls:
			# try:
				# found_html = get_html(found_url)
				# get_frqnt_content(found_html,found_url)
			# except:
				# print('异常url：' + found_url)
				# write_item(found_url)
				# break
if __name__ == '__main__':
	main()