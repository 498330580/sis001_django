import os
import sys
import requests as req
from bs4 import BeautifulSoup
import re
import cn2an
import time
from random import randint

# 公共变量
# 获取环境变量
# 获取当前运行环境
if os.getenv('os') == "docker":
    """docker系统运行的情况"""
    print("docker运行")
    cookies = os.getenv('COOKIES')
    proxy_type = os.getenv('PROXY_TYPE')
    proxy_url = os.getenv('PROXY_URL')
else:
    """普通系统运行情况"""
    print('普通模式运行')
    cookies = "cdb2_cookietime=0; _ga=GA1.2.583183031.1625137140; __utmz=55300009.1625143111.1.1.utmcsr=(direct)|utmccn=(" \
              "direct)|utmcmd=(none); cdb2_smile=1D1; Hm_lvt_68e9efc1d4049211a96bbbe6435e8498=1625226144; " \
              "HstCfa4580465=1631341225825; HstCmu4580465=1631341225825; HstCns4580465=1; HstCnv4580465=1; " \
              "HstCla4580465=1631341686431; HstPn4580465=20; HstPt4580465=20; cdb2_readapmid=438D433D435; " \
              "cdb2_sid=1LLCWZ; __utma=55300009.583183031.1625137140.1641824638.1641867202.25; __utmc=55300009; " \
              "__utmb=55300009.1.10.1641867202; cdb2_uvStat=1641867368; " \
              "cdb2_auth=hV47rzhgxRYQfiX82y1nm8e2KNITZ23zMwZrgAgLFZbJJi8ZoePzezTwjoGjdG0R1hlgpVqdKqfnXA8j; " \
              "cdb2_oldtopics=D11209689D"    # cookies
    proxy_type = "http"     # 代理类型 socks5 http
    proxy_url = "127.0.0.1:7890"      # 代理地址
Max_sleep = 5  # 最大等待时间

# 引入django环境
pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd + "../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sis001_django.settings")
import django
django.setup()
from xiaosuo.models import *
from users.models import UserProfile
user = UserProfile.objects.get(username="498330580")


# 整理未取得作者的小说
def get_authur(content, title):
    pattern = re.compile(r'作者：(.*?)\n')
    zuozhe = re.search(pattern, content, flags=0)
    if not zuozhe:
        """如果文章中未获取到作者信息，就从文章标题中获取"""
        pattern = re.compile(r'作者：(.*?)$')
        zuozhe = re.search(pattern, title, flags=0)
    if zuozhe:
        authur = zuozhe.group(1)
    else:
        authur = "无"
    return authur


# 去掉头部作者、字数信息
# 内容处理中间件（去掉无关信息）
def del_author_num(data):
    # a = re.compile(r'作者[\S\s].*', re.M)
    # data = re.sub(a, "", data)
    # a = re.compile(r'字数[\S\s].*', re.M)
    # data = re.sub(a, "", data)
    # a = re.compile(r'\S*?作者[\S\s]+字数[\S\s].*', re.M)
    # a = re.compile(r'版主提醒[\S\s]+', re.M)
    # data = re.sub(a, "", data)
    # a = re.compile(r'\S*?作者[\S\s]+?字数\S+', re.M)
    # data = re.sub(a, "", data)

    # a = re.compile(r'是否首发[\S\s].*', re.M)
    # data = re.sub(a, "", data)
    # a = re.compile(r'首发网站[\S\s].*', re.M)
    # data = re.sub(a, "", data)
    # a = re.compile(r'[\S\s]*发表于[\S\s]*', re.M)
    # data = re.sub(a, "", data)
    # a = re.compile(r'[\S\s]*首发于[\S\s]*', re.M)
    # data = re.sub(a, "", data)
    # a = re.compile(r'^\d+\.\d+\.\d+', re.M)
    # data = re.sub(a, "", data)
    # a = re.compile(r'^\[[\S\s]+\]', re.M)
    # data = re.sub(a, "", data)
    return data.strip()


# 等待时间
def time_sleep(s, m=Max_sleep):
    sec = randint(s, m)
    # print(f"等待{sec}秒")
    time.sleep(sec)


# 检测cookies是否添加
def is_cookies():
    if cookies == 'cookies':
        print('请添加cookies')
        return False
    else:
        return True


# 检测代理
def test_proxies():
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/67.0.3396.99 Safari/537.36"}
    if proxy_type == "http":
        proxy = {
            "http": f"http://{proxy_url}",
            "https": f"https://{proxy_url}",
        }
    else:
        proxy = {
            "http": f"socks5://{proxy_url}",
            "https": f"socks5://{proxy_url}",
        }
    try:
        response = req.get("http://www.sis001.com/", headers=header, proxies=proxy, timeout=30, verify=False)

        if response.status_code == 200:
            # print("该代理IP可用：",proxies)
            return True
        else:
            print("该代理IP不可用，请更换或开启代理")
            return False
    except Exception as e:
        print("代理出错error:", e)
        print("该代理IP无效：", proxy_url)
        return False


# sis网站爬取
class Sis001:
    def __init__(self):
        self.headers = {
            "User-Agent": r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          r"Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55",
            "Cookie": cookies,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        if proxy_type == "http":
            self.proxies = {
                "http": f"http://{proxy_url}",
                "https": f"https://{proxy_url}",
            }
        else:
            self.proxies = {
                "http": f"socks5://{proxy_url}",
                "https": f"socks5://{proxy_url}",
            }

    def get_html(self, url):
        """
        获取html
        :param url:
        :return:
        """
        # print(f"正在获取  {url}  源码")
        time_sleep(2)
        data = req.get(url=url, headers=self.headers, proxies=self.proxies, stream=True)
        soup = BeautifulSoup(data.text, 'html.parser')
        return soup

    def get_content(self, url):
        """
        爬取详情页
        :param url:
        :return:
        """
        try:
            html = self.get_html(url)
            # print(f"正在获取详情页 {url} 数据")
            bankuai = html.find("div", attrs={"id": "nav"}).find_all("a")[-1].text
            h1 = html.find("h1")
            if len(h1.contents) > 1:
                try:
                    tag = h1.contents[0].text.strip("[").strip("]")
                except:
                    tag = "无"
                title = h1.contents[1].text
            else:
                tag = "无"
                title = h1.contents[0].text
            # 转换标题
            title = cn2an.transform(title, "cn2an")
            content = self.get_text(html)
            authur = get_authur(content, title)
            content = del_author_num(content)

            data = dict(tag=tag.strip(),
                        bankuai=bankuai.strip(),
                        content=content.strip(),
                        authur=authur.strip())
            return data
        except Exception as e:
            print(f"爬取详情页 {url} ERROR： {e}")
            return False

    def get_text(self, html) -> str:
        """
        爬取内容
        :param html:
        :return:
        """
        data = ""

        content = html.find_all("div", attrs={"class": "t_msgfont noSelect"})
        for i in content:
            if i.table:
                i.table.decompose()
            if i.strong:
                i.strong.decompose()
            if len(i.text) > 500:
                data = data + i.text.strip() + "\n"

        pages = html.find("div", attrs={"class": "pages"})
        if pages:
            pages = pages.find("a", attrs={"class": "next"})
            if pages:
                content = data + self.get_text(self.get_html(f"http://www.sis001.com/forum/{pages['href']}"))
                return content
            else:
                return data
        else:
            return data


# 获取板块ID
def get_bankuai(name: str) -> Plate:
    bankuai_all = Plate.objects.filter(name=name)
    if bankuai_all.count():
        bankuai = bankuai_all[0]
    else:
        bankuai = Plate(user=user, name=name)
        bankuai.save()
    return bankuai


# 获取tag id
def get_tag(tag_name: str, bankuai_name: str) -> (Classification, Plate):
    bankuai = get_bankuai(bankuai_name)
    tag_all = Classification.objects.filter(name=tag_name, bk__name=bankuai_name)
    if tag_all.count():
        tag = tag_all[0]
    else:
        tag = Classification(user=user, name=tag_name, bk=bankuai)
        tag.save()
    return tag, bankuai


# 数据库操作
def save_data():
    data_all = Chapter.objects.filter(crawling_status=False)
    if data_all.count():
        sis001 = Sis001()
        count = 1
        print(f"当前数据库中有{data_all.count()}条数据需要爬取")
        for data in data_all:
            print(f"正在爬取第{count}/{data_all.count()}条数据：{data.url}")

            sis001_data = sis001.get_content(data.url)
            # bankuai = get_bankuai(sis001_data["bankuai"])
            # print(sis001_data)
            if sis001_data:
                tag, bankuai = get_tag(sis001_data["tag"], sis001_data["bankuai"])
                zuozhe = sis001_data["authur"]
                neirong = sis001_data["content"]
                jianjie = neirong.strip()[:250] + "..."

                zhangjie = Chapter.objects.filter(url=data.url)
                zhangjie.update(authur=zuozhe, classification=tag, plate=bankuai, introduction=jianjie, content=neirong, crawling_status=True)

                book = Collection.objects.filter(chapter__url=data.url)
                book.update(authur=zuozhe, classification=tag, plate=bankuai, introduction=jianjie)

                user_book = CollectionCount.objects.filter(collection__in=book)
                if user_book.count():
                    user_book.update(yikan=False)
            else:
                print('爬取详情失败，请检查代码！！！')
            count += 1
    else:
        print(f"数据库中没有数据需要爬取")


# 主函数
def main():
    print("--------------爬取开始--------------")
    if test_proxies():
        if is_cookies():
            save_data()
    else:
        print("请打开代理")
    print("--------------爬取完成--------------")


# # 临时函数，去除多余tag与bankuai
# def del_tag_bankuai():
#     tag_list = []
#     bankuai_list = []
#     for tag in Chapter.objects.all():
#         if tag.classification.id not in tag_list:
#             tag_list.append(tag.classification.id)
#         if tag.plate.id not in bankuai_list:
#             bankuai_list.append(tag.plate.id)
#     for bankuai in Collection.objects.all():
#         if bankuai.classification.id not in tag_list:
#             tag_list.append(bankuai.classification.id)
#         if bankuai.plate.id not in bankuai_list:
#             bankuai_list.append(bankuai.plate.id)
#     # print(tag_list, len(tag_list))
#     # print(bankuai_list, len(bankuai_list))
#
#     for tag in Classification.objects.all():
#         if tag.id not in tag_list:
#             print(tag.name)
#             tag.delete()
#
#     for bankuai in Plate.objects.all():
#         if bankuai.id not in bankuai_list:
#             print(bankuai.name)
#             bankuai.delete()


# # 处理简介信息，将简介减少为50个字符
# def jianjie_50():
#     for i in Collection.objects.all():
#         jianjie = i.introduction
#         i.introduction = jianjie[:50] + "..."
#         i.save()
#
#     for i in Chapter.objects.all():
#         jianjie = i.introduction
#         i.introduction = jianjie[:50] + "..."
#         i.save()


# # 整理用户阅读历史
# def zhengli_user_lishi():
#     for user_book in CollectionCount.objects.all():
#         user_zj = ChapterCode.objects.filter(chapter__collection=user_book.collection).order_by("-update_time")
#         if user_zj.count() > 0:
#             print(user_zj[0])
#             user_book.jindu = user_zj[0]
#             user_book.save()


# # 整理分类数据
# def fenlei_zl():
#     for zj in Chapter.objects.all():
#         tag = Classification.objects.filter(name=zj.classification.name, bk__name=zj.plate.name)
#         if tag.count() <= 0:
#             print(f"板块:{zj.plate.name}---分类:{zj.classification.name}")
#             fenlei = Classification(name=zj.classification.name, bk=zj.plate, user=user)
#             fenlei.save()


# # 整理已看小说
# def zhengl_look_book():
#     for i in CollectionCount.objects.all():
#         user_to_zj = ChapterCode.objects.filter(user=i.user, chapter__collection=i.collection)
#         if user_to_zj.count() == Chapter.objects.filter(collection=i.collection).count():
#             # 存在用户章节记录，并且记录与章节数相同
#             if not user_to_zj.filter(look_code__lt=1).count():
#                 print("已看完", i)
#                 i.yikan = True
#                 i.save()


if __name__ == "__main__":
    # del_tag_bankuai()
    # jianjie_50()
    # zhengli_user_lishi()
    # fenlei_zl()
    # zhengl_look_book()
    main()
