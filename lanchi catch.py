import math
import threading
import time
import os
import requests
from bs4 import BeautifulSoup
from urllib3.connectionpool import xrange
from bypy import ByPy
bp = ByPy()
bp.mkdir(remotepath='lc')
 
def split_list(ls, each):
    list = []
    eachExact = float(each)
    groupCount = int(len(ls) // each)
    groupCountExact = math.ceil(len(ls) / eachExact)
    start = 0
    for i in xrange(each):
        if i == each - 1 & groupCount < groupCountExact:  # 假如有余数，将剩余的所有元素加入到最后一个分组
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
    soup = BeautifulSoup(html)#BeautifulSoup和request搭配使用更佳呦
    itemBox = soup.find_all('div', attrs={'class': 'itemBox'})#find_all返回的是一个list
    for index, item in enumerate(itemBox):#遍历itemBox，index是当前项list的下标，item是内容
        itemTxt = item.find('div', attrs={'class': 'itemTxt'})#因为只有一个，所以itemBox中只有一个itemTxt所以这次我们用find
        a = itemTxt.find('a', attrs={'class': 'title'})
        chapter_url = a['href']
        chapter_url_list.append(chapter_url)#把所有书的url存起来
        print(str(index+1)+'.'+a.text)
    number = 1
    chapter_html_list = BeautifulSoup(get_document(chapter_url_list[number-1]))#因为打印的序号和list的索引是相差1的,所以输入的序号减一获取对应书的url，再根据url获取到目录页面
    ul = chapter_html_list.find('ul', attrs={'id': 'chapter-list-1'})#获取到ul
    book_name = chapter_html_list.find('h1', attrs={'class': 'title'}).text#获取到ul
    li_list = ul.find_all('li')#获取其中所有li
    for li in li_list:#遍历
        li_a_href = li.find('a')['href']#注意这里获取到的url是不完整的/manhua/buhuochongwuniangdezhengquefangfa/1000845.html
        i = 1
        path = "f:/"+book_name+'/'+li.text.replace('\n', '')
        if not os.path.exists(path):
            os.makedirs(path)
            bp.mkdir(remotepath=li.text.replace('\n', ''))
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
            open(path+'/'+li.text.replace('\n', '')+';'+str(i)+'.jpg', 'wb').write(get_document(img_src))#保存到d:/SanMu/书名/章节名/0.jpg
            bp.upload(localpath=path+'/'+li.text.replace('\n', '')+';'+str(i)+'.jpg',remotepath='lc',ondup='newcopy')
            os.remove(path+'/'+li.text.replace('\n', '')+';'+str(i)+'.jpg')
            i += 1
 
 
download_img(get_document("https://m.gufengmh8.com/search/?keywords=蓝翅"))