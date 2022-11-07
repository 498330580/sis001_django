import os
import pickle
import sys
import re
import time
from random import randint
import requests as req

# import pymongo
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

webdriver.ChromeOptions()

# 设定工作目录为当前脚本目录
jaoben_path = os.path.abspath(os.path.dirname(sys.argv[0]))  # 当前脚本目录
os.chdir(jaoben_path)  # 设定工作目录为脚本目录

# 全局变量
Chrome_path = os.path.join(jaoben_path, "chrome", "chrome.exe")  # 浏览器路径
Driver_path = os.path.join(jaoben_path, "chrome", "chromedriver.exe")  # 浏览器驱动路径
Cookie_data_path = os.path.join(jaoben_path, "data", "cookie")  # cookie数据储存地址
# Download_path = os.path.join(jaoben_path, "download")    # 下载目录
Proxy_server = "http://127.0.0.1:10809"  # 代理
User_Password = ["498330580", "19920124zhy@."]
Max_sleep = 5  # 爬取最大等待时间
Login_yanzheng_url = "http://www.sis001.com//forum/forum-184-1.html"  # 登陆验证地址
Token_data = "Token 27171cc46f6bda2668ca755810635e577f600fa4"
Api_host = "http://sis001.yaoling.ltd/"
headers = {"Content-type": "application/json",
           "Authorization": Token_data
           }


# # 引入django环境
# pwd = os.path.dirname(os.path.realpath(__file__))
# sys.path.append(pwd + "../")
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sis001_django.settings")

# import django
# django.setup()

# from xiaosuo.models import *
# from users.models import UserProfile
# user = UserProfile.objects.get(username="498330580")


# 等待时间
def time_sleep(s, m=Max_sleep):
    sec = randint(s, m)
    print(f"等待{sec}秒")
    time.sleep(sec)


# 爬取类
class Get_sis001_xiaosuo:
    def __init__(self):
        options = Options()
        options.binary_location = Chrome_path
        options.add_argument(f'--proxy-server={Proxy_server}')
        options.add_argument(
            'user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/69.0.3497.100 Safari/537.36"')  # 配置对象添加替换User-Agent的命令
        options.add_argument('window-size=800x600')  # 设置浏览器分辨率（窗口大小）
        # options.add_argument('url=http://www.baidu.com')
        options.add_argument('disable-infobars')  # 禁用浏览器正在被自动化程序控制的提示
        options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片
        options.add_argument("--disable-gpu")  # 禁用gpu
        options.add_argument('--start-minimized')  # 最小化运行
        options.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
        options.add_experimental_option('excludeSwitches', ['enable-logging'])  # 禁止打印日志
        options.add_argument("disable-cache")  # 禁用缓存
        options.add_argument('log-level=3')  # INFO = 0 WARNING = 1 LOG_ERROR = 2 LOG_FATAL = 3 default is 0
        self.driver = webdriver.Chrome(chrome_options=options, executable_path=Driver_path)
        # self.driver.set_window_size(800, 600)
        self.driver.minimize_window()
        self.login_panduan = 0

    def login(self):
        # 判断是否登录，未登录则直接登录
        if not self.login_panduan:
            self.driver.get(Login_yanzheng_url)
            con = 0
            while "您还没有登录" in self.driver.find_element_by_xpath('//*[@id="wrapper"]/div[1]/div[4]/p[3]').text:
                # if con > 0:
                #     print("登陆失败")
                con += 1
                if con >= 3:
                    input("无法自动登陆，等待用户手动操作，操作完成后请按回车键")
                    # 用户手动登陆后储存新的cookie
                    self.driver.get_cookies()
                    with open(Cookie_data_path, "wb") as f:
                        pickle.dump(self.driver.get_cookies(), f)
                    self.login_panduan = 1
                time_sleep(2)
                if os.path.exists(Cookie_data_path) and con < 2:
                    print("使用cookie信息登陆")
                    with open(Cookie_data_path, "rb") as f:
                        cookie_list = pickle.load(f)
                    for i in cookie_list:
                        self.driver.add_cookie(i)
                    self.driver.refresh()
                    if "您还没有登录" in self.driver.find_element_by_xpath('//*[@id="wrapper"]/div[1]/div[4]/p[3]').text:
                        print("cookie登录失败")
                    else:
                        print("cookie登陆成功")
                        # 登陆成功后储存新的cookie
                        time_sleep(2)
                        self.driver.get_cookies()
                        with open(Cookie_data_path, "wb") as f:
                            pickle.dump(self.driver.get_cookies(), f)
                        self.login_panduan = 1
                else:
                    print("模拟登陆")
                    self.driver.get('http://www.sis001.com//forum/logging.php?action=login')
                    self.driver.implicitly_wait(30)
                    em_data = self.driver.find_element_by_xpath('//*[@id="clickVerifyDiv"]').find_elements_by_tag_name(
                        "em")
                    int_or_en = self.driver.find_element_by_xpath('//*[@id="verifyTips"]/font').text
                    for i in em_data:
                        if "数字" == int_or_en and str(i.text).isdigit():
                            i.click()
                        elif "字母" == int_or_en and str(i.text).isalpha():
                            i.click()

                    self.driver.find_element_by_xpath('//*[@id="username"]').send_keys(User_Password[0])
                    self.driver.find_element_by_xpath('//*[@id="nextBtn"]').click()
                    self.driver.find_element_by_xpath('//*[@id="confirmYes"]/tr[1]/td/label[5]/input').click()
                    self.driver.find_element_by_xpath('//*[@id="password"]').send_keys(User_Password[1])
                    time_sleep(2)
                    self.driver.find_element_by_xpath('//*[@id="loginsubmit"]').click()
                    # 登陆成功后储存新的cookie
                    time_sleep(2)
                    self.driver.get(Login_yanzheng_url)
                    if "您还没有登录" in self.driver.find_element_by_xpath('//*[@id="wrapper"]/div[1]/div[4]/p[3]').text:
                        print("模拟登陆失败")
                    else:
                        print("模拟登陆成功")
                        time_sleep(2)
                        self.driver.get_cookies()
                        with open(Cookie_data_path, "wb") as f:
                            pickle.dump(self.driver.get_cookies(), f)
                        self.login_panduan = 1
            else:
                print("通过页面判断为已登录")
                self.login_panduan = 1
        else:
            print("浏览器为已登录状态")

    def get_html(self, url):
        self.login()
        self.driver.get(url)

    def get_url(self, url):
        if "sis001" in url:
            self.get_html(url)
            data = {'title': self.driver.find_element_by_xpath('//*[@id="wrapper"]/div[1]/form/div[1]/h1').text}
            data_list = []
            while True:
                content = self.driver.find_elements_by_xpath(
                    '/html/body/div[4]/div[1]/form/div/table/tbody/tr[1]/td[2]/div[3]/div[3]/div')
                for i in content:
                    if len(i.text) > 500:
                        data_list.append(i.text)
                nextpage = self.driver.find_elements_by_css_selector(
                    '#wrapper > div:nth-child(1) > div:nth-child(12) > div.pages > a.next')
                if len(nextpage) == 1:
                    self.driver.find_element_by_css_selector(
                        '#wrapper > div:nth-child(1) > div:nth-child(12) > div.pages > a.next').click()
                else:
                    break
                    # print("››")
            data['data'] = data_list
            return data
        else:
            print("输入的不是sis001的网址，请重新输入")
            return False

    def sis001_exit(self):
        self.driver.close()


# 检测代理
def test_proxies(proxies):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/67.0.3396.99 Safari/537.36"}
    try:
        response = requests.get(Login_yanzheng_url, headers=header, proxies={"http": proxies}, timeout=5)
        if response.status_code == 200:
            # print("该代理IP可用：",proxies)
            return True
        else:
            print("该代理IP不可用，亲更换或开启代理")
            return False
    except Exception as e:
        print("代理出错error:", e)
        print("该代理IP无效：", proxies)
        return False


# 获取数据并储存数据库
class Get_Xiaosuo:
    def __init__(self):
        self.sis001 = Get_sis001_xiaosuo()

    def get_save(self):
        zhangjie = Chapter.objects.filter(crawling_status=False)
        print(f'当前数据库中共有{zhangjie.count()}条数据未爬取')
        index = 0
        pattern = re.compile(r'^(版主.*?)作者：', re.S)
        for chapter in zhangjie:
            index += 1
            print(f"正在爬取第{index}条：", chapter)
            data = self.sis001.get_url(chapter.url)
            t = ""
            for xiaosuo_str in data['data']:
                t = t + xiaosuo_str

            # 去除文章中的广告
            guanggao = pattern.findall(t)
            if guanggao:
                for i in guanggao:
                    t = t.replace(i, "")

            chapter.content = t
            chapter.crawling_status = True
            chapter.save()
        print("爬取完毕")
        self.sis001.sis001_exit()


# 整理未取得作者的小说
def get_authur():
    chapters = Chapter.objects.filter(authur="无")
    collections = Collection.objects.filter(authur="无")
    if chapters or collections:
        print("正在整理作者信息")
        if chapters:
            for chapter in chapters:
                pattern = re.compile(r'作者：(.*?)\n')
                zuozhe = re.search(pattern, chapter.content, flags=0)
                if zuozhe:
                    print(f"章节：{chapter.name}--作者信息缺失--添加作者{zuozhe.group(1)}")
                    chapter.authur = zuozhe.group(1)
                    chapter.save()

        if collections:
            for collection in collections:
                zhangjie = Chapter.objects.filter(collection=collection).order_by("index")[0]
                if zhangjie.authur != "无":
                    print(f"书籍：{collection.name}--作者信息缺失--添加作者{zhangjie.authur}")
                    collection.authur = zhangjie.authur
                    collection.save()
        print("作者信息整理完毕")


# 整理文章信息
def get_content():
    print("正在整理文章信息")

    for zj in req.get(url=Api_host+"zhangjie", headers=headers).json()["results"]:
        print(zj)

    # for chapter in Chapter.objects.all():
    #     content = chapter.content
    #     pattern = re.compile(r'^(版主.*?)作者：', re.S)
    #     guanggao = pattern.findall(content)
    #     if guanggao:
    #         print(f"章节：{chapter.name}--内容整理--去除版主广告")
    #         for i in guanggao:
    #             content = content.replace(i, "")
    #         chapter.content = content
    #         chapter.introduction = content[:150]
    #         chapter.save()
    print("整理文章信息完毕")


# 添加文章简介
def add_introduction():
    zhangjie_introduction = Chapter.objects.filter(introduction="无")
    book_introduction = Collection.objects.filter(introduction="无")
    if zhangjie_introduction or book_introduction:
        print("正在整理文章简介")
        if zhangjie_introduction:
            for zj in zhangjie_introduction:
                zj.introduction = zj.content[:150]
                zj.save()
        if book_introduction:
            for book in book_introduction:
                book.introduction = Chapter.objects.filter(collection=book).order_by("index")[0].introduction
                book.save()
        print("整理文章简介完毕")


def main():
    while True:
        if test_proxies(Proxy_server):
            mongo = Get_Xiaosuo()
            mongo.get_save()
            get_content()
            add_introduction()
            get_authur()
        else:
            print("请打开代理")
        sec = 1
        print(f"等待{sec}分钟")
        time.sleep(sec * 60)


if __name__ == "__main__":
    # main()
    headers = {"Content-type": "application/json",
               "Authorization": Token_data
               }
    r = req.get(url=Api_host + "panduan?type=xiaosuo&url=http://www.sis001.com/forum/thread-11045018-1-1.html",
                headers=headers).json()
    print(r)
