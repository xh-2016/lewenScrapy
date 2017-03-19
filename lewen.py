#coding=utf-8

from selenium import webdriver
import selenium.webdriver.support.ui as ui
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen

downloadDir = 'D:\\py35\\copyTxt\\'#下载后存放目录

class lewen():
    
    #搜索小说，定位到目标小说页:返回一个章节链接的列表
    def search(bookName):
        driver = webdriver.Firefox()
        base_url = "http://www.lewenxiaoshuo.com"
        driver.get(base_url)
        driver.find_element_by_id("searchkey").clear()
        driver.find_element_by_id("searchkey").send_keys(bookName)#这里可以改成传参:摇欢
        driver.find_element_by_id("searchsubmit").click()
        #解决报错：元素不能定位，等待5秒。直到元素可以定位
        wait = ui.WebDriverWait(driver,5)
        wait.until(lambda driver: driver.find_element_by_xpath(".//*[@id='main']/div[1]/ul/li/span[2]/a"))
        a = driver.find_element_by_xpath(".//*[@id='main']/div[1]/ul/li/span[2]/a")
        target_href = a.get_attribute("href")  #获取目标小说的链接
        print("目标小说链接：" + target_href)
        now_handle = driver.current_window_handle #初始窗口
        print("初始窗口：" + now_handle)
        a.click()  #进入新的窗口
        driver.implicitly_wait(20)
        
        all_handles = driver.window_handles #获取所有窗口句柄
        for handle in all_handles:
            if handle != now_handle:
                #输出待选择的窗口句柄
                print("新窗口：" + handle)
                driver.switch_to_window(handle)#跳转到新的窗口
                time.sleep(1)        
        #print(all_handles[1])这种写法数组越界，不造为嘛
                
        #urls = driver.find_element_by_xpath(".//*[@id='list']/dl/dd[1]/a")#通过css_selector定位不到，不造为嘛
        a_s = driver.find_elements_by_xpath(".//*[@id='list']/dl/dd[*]/a")#获取小说所有章节链接列表所在的标签a
        driver.implicitly_wait(20)
        urls = [] #保存小说所有章节链接列表
        #由于小说的章节链接地址不连续的，故需要保存所有章节链接
        for a in a_s:
            chapter_href = a.get_attribute("href")#章节链接
            #chapter_title = a.get_attribute("title")#章节标题           
            urls.append(chapter_href)           
        print("小说章节总数：",len(urls))
        return urls
        
    #按章节通过链接爬取小说
    def get_name_content(urls):       
        chapters = []
        for url in urls:
            response = urlopen(url)
            html = response.read()
            soup = BeautifulSoup(html,"html5lib")
            title = soup.findAll('h1')[0].text          
            print("爬取章节：" + title)
            chapters.append(title)
            content = soup.findAll(id="content")[0]               
            for string in content:
                st = str(string)              
                #st = string.__str__()，和上面函数功能相同
                if (len(st.split('<br/>')) > 1):#不太懂！！
                    pass
                else:
                    chapters.append(st)                
        return chapters
    
    #清洗文本格式，一次性写入txt文件：关键是调整格式
    def save_book(bookName,chapters):
        now =time.strftime("%Y%m%d%H%M%S", time.localtime())#当前时间，纯字符串格式
        bookname = downloadDir  + bookName + now + '.txt'       
        file = open(bookname, 'w+', encoding='utf-8')
        for i in chapters:        
            #file.write('\t')
            for ii in i.split('  '):#i.split('  ')用多个空白符分割字符串，保留一个空格部分；''表示空，
                if ii.startswith('<div'):#去掉每章开头多余的<div……></div>
                    ii = ""
                ii = ii.replace("<p></p>","")  #去掉每章最后多余的<p></p>              
                file.write(ii)
            file.write('\n')  #每写完一句，换行，控制文本格式  
               
if __name__ == "__main__":
    chapter_urls = lewen.search("我从来没有谈过恋爱")
    chapters = lewen.get_name_content(chapter_urls)
    lewen.save_book("我从来没有谈过恋爱",chapters)
    
