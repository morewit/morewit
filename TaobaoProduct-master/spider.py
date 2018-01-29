#import pymongo
#from pymongo import MongoClient
import sqlite3

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery as pq
from config import *
from urllib.parse import quote

#browser = webdriver.Chrome()
# browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)
SERVICE_ARGS = ['--load-images=false', '--disk-cache=true']
browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
#browser = webdriver.Chrome(chrome_options=chrome_options)

wait = WebDriverWait(browser, 10)

#用sqlite3 如果文件不存在，会自动在当前目录创建:
conn = sqlite3.connect('test.db')
# 创建一个Cursor:
cursor = conn.cursor()
# 执行一条SQL语句，创建user表:
try:
    cursor.execute('create table productb (item varchar(20)  primary key,title varchar(50), price varchar(20),location varchar(20))')
except:
    print('Create table failed')
    pass

def index_page(page):
    """
    抓取索引页
    :param page: 页码
    """
    print('正在爬取第', page, '页')
    try:
        url = 'https://s.taobao.com/search?q=' + quote(KEYWORD)
        browser.get(url)
        if page > 1:
            input = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager div.form > input')))
            submit = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager div.form > span.btn.J_Submit')))
            input.clear()
            input.send_keys(page)
            submit.click()
        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager li.item.active > span'), str(page)))
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-itemlist .items .item')))
        get_products()

    except TimeoutException:
        index_page(page)


def get_products():
    """
    提取商品数据
    """
    html = browser.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    rownum = 0
    for item in items:
        product = {
            'title':item.find('.title').text(),
            'price': item.find('.price').text(),
            'location':item.find('.location').text()
        }
        print(product['title'],product['price'],product['location'])
        #v = puoduct
        ins = "insert into productb values(?,?,?,?);"
        cursor.execute(ins, (str(rownum),str(product['title']),str(product['price']),str(product['location'])))
        rownum = rownum +1
        # 提交事务:
        conn.commit()

def main():
    """
    遍历每一页
    """
    #for i in range(1, MAX_PAGE + 1):
    for i in range(1, 2):
        index_page(i)
    cursor.close()
    # 关闭Connection:
    conn.close()
    browser.close()


if __name__ == '__main__':
    main()
