import sqlite3
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery as pq
from config import *

from urllib.parse import quote

#采用Chrome headless 须安装Chrome浏览器和与之匹配的Chromedriver.exe，并设置环境变量
from selenium.webdriver.chrome.options import Options
global browser

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
browser = webdriver.Chrome(chrome_options=chrome_options)
"""
#采用PhantomJS,但已慢慢开始被放弃
SERVICE_ARGS = ['--load-images=false', '--disk-cache=true']
browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)
"""
wait = WebDriverWait(browser, 10)
conn = sqlite3.connect('test.db')#用sqlite3 如果文件不存在，会自动在当前目录创建:
cursor = conn.cursor()# 创建一个Cursor:

browser.get('http://www.cdggzy.com')
time.sleep(1)
xmlxnamelist = ['JSGC','ZFCG','LandTrade','AssetResource']
xmlxurllist = []
for link in browser.find_elements_by_xpath("//*[@href]"):
    for xmlx in xmlxnamelist:
        if (link.get_attribute('href')).find(xmlx)>0 and xmlxurllist.count(link.get_attribute('href'))==0:
            xmlxurllist.append(link.get_attribute('href'))
        else:
            pass
#print(xmlxurllist)
"""
#获取项目类型的链接 方法一
urlJSGC = browser.find_element_by_xpath("//*[@id='form1']/div[3]/div[2]/div[2]/div/div[1]/div[1]/a").get_attribute('href')
urlLand = browser.find_element_by_xpath("//*[@id='form1']/div[3]/div[2]/div[2]/div/div[1]/div[2]/a").get_attribute('href')
urlReso = browser.find_element_by_xpath("//*[@id='form1']/div[3]/div[2]/div[2]/div/div[1]/div[3]/a").get_attribute('href')
urlZFCG = browser.find_element_by_xpath("//*[@id='form1']/div[3]/div[2]/div[2]/div/div[1]/div[4]/a").get_attribute('href')
#赋予项目类型的链接
url = ['http://www.cdggzy.com/site/JSGC/List.aspx',
     'http://www.cdggzy.com/site/Notice/ZFCG/NoticeList.aspx',
     'http://www.cdggzy.com/site/LandTrade/LandList.aspx',
     'http://www.cdggzy.com/site/AssetResource/DealNoticeList.aspx']
"""
url = xmlxurllist #[urlJSGC,urlZFCG,urlLand,urlReso]
xmlxlist = ['建','采','土','资']
urltext = url[0]
xmlx = xmlxlist[0]
url_database_text ='create table IF NOT EXISTS gonggaob (item varchar(20)  ,quxian varchar(6),infotitle varchar(50),baoming varchar(10), publishtime varchar(20))'

""" #读取表名
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';") 
tablenames = (cursor.fetchall())
print(tablenames)
"""
try:
    cursor.execute(url_database_text)  # 执行一条SQL语句，创建user表:
    cursor.execute('delete  from  gonggaob  where 1=1')  # 清空表格
except:

    print('Create table failed')
    pass
def index_page(page):

    try:
        for i in range(len(xmlxurllist)):#爬取项目类型range(2):
            urltext=url[i]
            #xmlx=xmlxlist[i]
            #print(xmlxlist[i])
            browser.get(urltext)
            browser.find_element_by_xpath("//div[@data-value='0']").click()  # 点击公告类型：全部公告
            browser.find_element_by_xpath("//div[@data-value='510112']").click()  # 点击交易地点：龙泉驿区
            time.sleep(5)

            pagestext = str(browser.find_element_by_xpath("//*[@id='LabelPage']").text)
            #pagestext = doc.find('#LabelPage').text()
            pageslist = pagestext.split('/')[:]
            #currentpage = int(pageslist[0])
            totalpages = int(pageslist[1])
            #print(pageslist)
            if page == 1:
                get_products(page, i)
            elif page <= totalpages:
                browser.find_element_by_xpath("//*[@id='Pager']/a[" + str(page + 1) + "]").click()
                time.sleep(5)
                #html = browser.page_source
                #doc = pq(html)
                #pagestext2 = str(browser.find_element_by_xpath("//*[@id='LabelPage']").text)
                #pagestext2 = doc.find('#LabelPage').text()
                #pageslist2 = pagestext2.split('/')[:]
                #print(pageslist2)
                """
                browser.find_element_by_xpath("//button[@id='preview']").click()  # 点击 上一页    
                browser.find_element_by_xpath("//button[@id='nextview']").click() # 点击 下一页
                """
                get_products(page, i)
            else:
                pass
            time.sleep(1)
    except TimeoutException:
        #index_page(page)
        pass
def get_products(page,i):
    time.sleep(1)  # 必须缓冲一下才行
    html = browser.page_source
    doc = pq(html)
    print(xmlxlist[i]+'：爬取第', page, '页 当前页：' + doc.find('#LabelPage').text())
    contentlist = doc('#contentlist .contentitem').items()
    content = doc('#contentlist').text()
    print(content)
    ins = "insert into gonggaob values(?,?,?,?,?);"
    rownum = 0
    for contentitem in contentlist:
        bm = contentitem.find('.item-right')
        bmtext = bm.text()
        if len(bmtext) == 10:
            bmtext = ''
        else:
            bmtext = bm.text()[-4:]  # 截取倒数第四个字符到结尾
        product = {
            'quxian': contentitem.find('.col-xs-1').text(),
            'infotitle': contentitem.find('.infotitle').text(),
            'baoming': bmtext,
            'publishtime': contentitem.find('.publishtime').text()
        }
        # print(product)
        cursor.execute(ins, (
        xmlxlist[i], product['quxian'], product['infotitle'], product['baoming'], product['publishtime']))
        rownum = rownum + 1
        conn.commit()

    #except:
    #    pass
def main():
    for i in range(3): #爬取页数1-3页
        index_page(i+1)
    cursor.close()

    conn.close() # 关闭Connection:
    browser.close()


if __name__ == '__main__':
    main()
