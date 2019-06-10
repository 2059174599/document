#很多需要完善的地方
from collections import Counter
import jieba
import requests
from multiprocessing import Pool
from bs4 import BeautifulSoup
import traceback
import re
import random
import pymysql

#关键词路径
path = 'D:\\python3.6\\name_key.txt'
#jieba分词路径
datapath = r'D:\python3.6\jieba_baike\围城.txt'

#分词模板
def cut_word(datapath):
    with open(datapath, 'r', encoding = 'gbk',errors='ignore') as f:
        string = f.read()
        #对文件中的非法字符进行过滤
        data=re.sub(r"[\s+\.\!\/_,$%^*(【】：\]\[\-:;+\"\']+|[+——！，。？、~@#￥%……&*（）《》]+|[0-9]+","",string)
        word_list = jieba.lcut(data)
        return word_list
        
#关键词 分词
def statistic_top_word(word_list):
    word_keys = []
    #统计每个单词出现的次数，别将结果转化为字典
    result= dict(Counter(word_list))
    for key in result.keys():
        if len(key) == 2: #只对双字词语百科
            word_keys.append(key)
    sums = len(word_keys)
    return word_keys[:1]
    #print(word_keys)
    
#关键词 文本
# def getKeyWord(path):
    # with open(path, 'r') as f:
       # lines = f.read()
       # for line in lines.strip().split():
           # yield line
           
#请求
def getHtmlText(url):
    head_user_agent = ['Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko', 
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)', 
    'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1', 'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3', 
    'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12', 'Opera/9.27 (Windows NT 5.2; U; zh-cn)', 'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
    'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)', 
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)', 
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.0.6.2000 Chrome/26.0.1410.43 Safari/537.1 ', 
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E; QQBrowser/7.3.9825.400)', 
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 ', 
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.92 Safari/537.1 LBBROWSER', 
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; BIDUBrowser 2.x)', 
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36']
    headers = {'User-Agent': random.choice(head_user_agent)}
    try:
        r = requests.get(url,headers = headers,timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        traceback.print_exc()
        return "请求错误"
        
#内容
def getContent(html,keyword):
    res_data={}
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.title.text
    print(title)
    summary = soup.find('div',class_='para').text
    sum = 1
    while title:
        res_data['title'] = title
        res_data['summary'] = summary
        res_data['keyword'] = keyword
    # if res_data:
        # sql = "INSERT INTO baike_word (word,summary,original_title) values('" + str(res_data['title'])+"','"+str(res_data['summary'])+"','"+str(res_data['keyword'])+"')"      
        # db_execute(sql)
    #print(res_data)
    #百科收录
    # if keyword in title:
        # pass
    #需要再次点击
    # elif
        # pass
    #百科未收录
    # else 
    
#链接数据库
def db_execute(sql):
    dbs = pymysql.connect(
                            host='localhost',
                            user='wxy', 
                            passwd='66357070', 
                            db='sys',
                            port=3306,
                            charset="utf8"
                        )
    cursor = dbs.cursor()
    try:
        dbs.autocommit(True)
        cursor.execute(sql)
    except:
   # Rollback in case there is any error
        dbs.rollback()
    cursor.close()
    
#主函数
def main(keyword):
    url = 'http://baike.baidu.com/search/word?word=' + keyword
    print(url)
    html = getHtmlText(url)
    content = getContent(html,keyword)
    #print(html[:1000])
    #for item in getparse(html):
        #print(item)
        
    
if __name__ =='__main__':
    word_list = cut_word(datapath)
    statistic_top_word(word_list)
    # for keyword in statistic_top_word(word_list):
        # main(keyword)
    #多进程
    pool = Pool()
    pool.map(main,[keyword for keyword in statistic_top_word(word_list)])