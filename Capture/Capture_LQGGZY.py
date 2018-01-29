# -*- coding: utf-8 -*-
#
# author: oldj <oldj.wu@gmail.com>
#

from selenium import webdriver
from PIL import Image
import time

def capture(url,save_fn2, save_fn="capture.png"):
    #browser = webdriver.Firefox()  # Get local session of firefox
    #SERVICE_ARGS = ['--load-images=false', '--disk-cache=true']
    #browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)
    browser = webdriver.PhantomJS()
    browser.set_window_size(1249, 900)
    #browser.set_window_size(1920, 1080)
    browser.get(url)  # Load page
    browser.execute_script("""
    (function () {
      var y = 0;
      var step = 100;
      window.scroll(0, 0);

      function f() {
        if (y < document.body.scrollHeight) {
          y += step;
          window.scroll(0, y);
          setTimeout(f, 50);
        } else {
          window.scroll(0, 0);
          document.title += "scroll-done";
        }
      }

      setTimeout(f, 500);
    })();
  """)

    #for i in xrange(30):
    #    if "scroll-done" in browser.title:
    #        break
    #    time.sleep(1)
    #browser.find_element_by_id("contentlist")

    browser.save_screenshot(save_fn)
    imgelement = browser.find_element_by_id('contentlist') #定位公告列表
    location =imgelement.location #获取列表x,y坐标
    size = imgelement.size #获取列表的长宽
    rangle = (int(location['x']), int(location['y']), int(location['x'] + size['width']),
             int(location['y'] + size['height']))  # 写成我们需要截取的位置坐标
    #rangle =(278,500,1160,900)
    i = Image.open("capture.png")  # 打开截图
    frame4 = i.crop(rangle)  # 使用Image的crop函数，从截图中再次截取我们需要的区域
    frame4.save(save_fn2)
    browser.close()

if __name__ == "__main__":
    capture("http://www.cdggzy.com/longquanyi/site/Notice/ZFCG/NoticeList.aspx","ZFCG.png")
    capture("http://www.cdggzy.com/longquanyi/site/JSGC/List.aspx", "JSGC.png")