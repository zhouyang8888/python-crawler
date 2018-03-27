
# -*- coding:utf8 -*-

#import scrapy
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import threading
import time
import sys 
import os
import urllib
from urllib import urlencode
import socket

reload(sys)
sys.setdefaultencoding('utf-8')

class BaiduSpider():
    '''
    爬取百度图片中的图片

    '''
    def __init__(self, search_keys):
        self.search_keys = search_keys
        self.url = 'http://image.baidu.com'
        self.page_total = 100
        self.socket_timeout = 60
        socket.setdefaulttimeout(self.socket_timeout)

    def Search(self):
        # 打开浏览器 ， 并在百度图片搜索中输入关键字
        self.download_dir = "/download/data-dir/crawl/" + self.search_keys
        print "download_dir : ", self.download_dir
        if os.path.exists(self.download_dir):
            os.removedirs(self.download_dir)
        os.makedirs(self.download_dir)
        prefs = {"download.default_directory":self.download_dir}
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument('--headless')
        chromeOptions.add_argument('--disable-gpu')
        chromeOptions.add_experimental_option("prefs", prefs) 
        driver = webdriver.Chrome(chrome_options=chromeOptions)
        driver.maximize_window()
        driver.get(self.url)
        inputElement = driver.find_element_by_name('word')
        inputElement.send_keys(self.search_keys)
        inputElement.submit()
        print 'Waiting results page.'
        time.sleep(10)
        print 'Go on.'
        return driver

    def download(self):
        driver = self.Search()

        page_total = self.page_total
        print 'Total page = ', page_total
        page_i = 0
        total_elements = 0
        remained_pics = [] # 标记已经处理过的图片元素

        while page_i < page_total:
            #elements_all = driver.find_elements_by_xpath('//ul/li/div/a/img')  # 一定是单引号
            imgurls = []
            elements_all = driver.find_elements_by_class_name('imgitem')  # 一定是单引号
            elements = elements_all

            # print elements
            i = 0
            print "Elements count:",  len(elements)
            for element in elements:			
                i += 1
                try:
                    # 去除重复图片
                    if element in remained_pics:
                        continue
                    
                    dataurl = element.get_attribute('data-objurl')
                    imgurls.append(dataurl)
                except Exception, e:
                    print 'Exception : ', str(e)
             
            action = ActionChains(driver).move_to_element(elements[-1])
            action.perform()
            
            action = ActionChains(driver).send_keys(Keys.DOWN)
            action.perform()
            
            page_i += 1
            #js = 'var q=document.body.scrollTop=' + bytes(page_i * 4) + "000"
            #driver.execute_script(js)
            
            remained_pics.extend(elements)
            
            for dataurl in imgurls:
                try:
                    print "[URL ]", dataurl
                    local_path = self.download_dir + "/" + dataurl.split("/")[-1]
                    print "[PATH]", local_path
                    urllib.urlretrieve(dataurl, local_path)
                     
                except Exception, e:
                    print 'Exception happend:', str(e)
                    threading._sleep(2)
            

            threading._sleep(5)

if __name__ == "__main__":
    query = sys.argv[1]
    spider = BaiduSpider(unicode(query))
    #spider = BaiduSpider(u'')
    spider.download()
