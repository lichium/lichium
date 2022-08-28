import math
import threading
import time
import os
import requests
from bs4 import BeautifulSoup # 第三方库
from urllib3.connectionpool import xrange
from bypy import ByPy # 第三方库，且须在cmd输入bypy info进行百度网盘绑定
bp = ByPy()
bp.mkdir(remotepath='lc')
 
def split_list(ls, each):
    list = []
    eachExact = float(each)
    groupCount = int(len(ls) // each)
    groupCountExact = math.ceil(len(ls) / eachExact)
    start = 0
    for i in xrange(each):
        if i == each - 1 & groupCount < groupCountExact:
            list.append(ls[start:len(ls)])
        else:
            list.append(ls[start:start + groupCount])
        start = start + groupCount
 
    return list
 
 
def get_document(url):
    # print(url)
    try:
        get = requests.get(url)
        data = get.content
        get.close()
    except:
        time.sleep(3)
        try:
            get = requests.get(url)
            data = get.content
            get.close()
        except:
            time.sleep(3)
            get = requests.get(url)
            data = get.content
            get.close()
    return data
 
 
def download_img(html):
    chapter_url_list=[]
    soup = BeautifulSoup(html)
    itemBox = soup.find_all('div', attrs={'class': 'itemBox'})
    for index, item in enumerate(itemBox):
        itemTxt = item.find('div', attrs={'class': 'itemTxt'})
        a = itemTxt.find('a', attrs={'class': 'title'})
        chapter_url = a['href']
        chapter_url_list.append(chapter_url)
        print(str(index+1)+'.'+a.text)
    number = int(input('请输入序号：'))
    chapter_html_list = BeautifulSoup(get_document(chapter_url_list[number-1]))
    ul = chapter_html_list.find('ul', attrs={'id': 'chapter-list-1'})
    book_name = chapter_html_list.find('h1', attrs={'class': 'title'}).text
    li_list = ul.find_all('li')
    for li in li_list:
        li_a_href = li.find('a')['href']
        i = 1
        path = "f:/"+book_name+'/'+li.text.replace('\n', '')
        if not os.path.exists(path):
            os.makedirs(path)
        while True:
            li_a_href_replace = li_a_href
            if i != 1:
                li_a_href_replace = li_a_href.replace('.', ('-' + str(i) + '.'))
            print(li_a_href_replace)
            chapter_html = BeautifulSoup(get_document('https://m.gufengmh8.com' + li_a_href_replace))
            chapter_content = chapter_html.find('div', attrs={'class': 'chapter-content'})
            img_src = chapter_content.find('img')['src']
            if img_src.__eq__('https://res.xiaoqinre.com/images/default/cover.png'):
                break
            chapter_content = chapter_html.find('div', attrs={'class': 'chapter-content'})
            img_src = chapter_content.find('img')['src']
            open(path+'/'+li.text.replace('\n', '')+';'+str(i)+'.jpg', 'wb').write(get_document(img_src))
            bp.upload(localpath=path+'/'+li.text.replace('\n', '')+';'+str(i)+'.jpg',remotepath='lc',ondup='newcopy') # 上传到百度网盘
            # os.remove(path+'/'+li.text.replace('\n', '')+';'+str(i)+'.jpg') # 欲删除下载到本地的内容可取消此行注释
            i += 1
 
 
download_img(get_document("https://m.gufengmh8.com/search/?keywords="+str(input('漫画名称：'))))