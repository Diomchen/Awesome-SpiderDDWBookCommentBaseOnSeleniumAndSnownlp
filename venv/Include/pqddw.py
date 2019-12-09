from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import quote
from pyquery import PyQuery as pq
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import pandas as pd



capa = DesiredCapabilities.FIREFOX
capa["pageLoadStrategy"] = "none" #懒加载模式，不等待页面加载完毕
# browser = webdriver.Chrome('D:\!文件下载目录\Chrome下载目录\chromedriver_win32\chromedriver.exe')
browser = webdriver.Firefox()#需要安装FirefoxDrive
wait = WebDriverWait(browser, 30) #等待的最大时间30s

def index_page(url,score_comment,page_num):
    try:
        while 1:
            print('正在爬取第{}页评论'.format(page_num))
            page_num += 1
            #获取网页页
            browser.get(url)
            #等待评论模块加载完毕
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#comment_list > div:nth-child(1)")))
            #加载完毕后立刻停止网页加载，提高速度
            browser.execute_script("window.stop();")  # 停止当前页面加载，防止input框输入错误
            time.sleep(5)
            #获取当前页面评论
            get_comment(score_comment)
            # 翻页
            browser.execute_script('document.querySelectorAll(".fanye a")[document.querySelectorAll(".fanye a").length - 1].click();')
            time.sleep(5)
    except Exception:
        #等无法翻页异常时，表示爬取完毕
        df = pd.DataFrame(score_comment)
        #转存excel文件
        df.to_excel('book_score_comment.xlsx')
    print("爬取完毕！")

def get_comment(score_comment):
    #获取网页加载出来的静态代码
    html = browser.page_source
    doc = pq(html)
    items = doc('#comment_list .item_wrap .comment_items').items()
    for item in items:
        product = {'score':item.find('em').text().split('分')[0],'comment':item.find('.describe_detail a').text()}
        score_comment.append(product)

if __name__ == '__main__':
    url = "http://product.dangdang.com/26924362.html"
    score_comment = []
    page_num = 1
    index_page(url,score_comment,page_num)
