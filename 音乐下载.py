import requests
import json
import os
import sys

choose = input("请选择下载源（单选，输入数字）：\n1  网易云音乐\n2  qq音乐\n> ")
id = input("请输入歌曲id/mid:\n> ")
session = requests.session()
if choose == '1':
    url = 'http://music.163.com/song/media/outer/url?id={id}'
elif choose == '2':
    searchurl = '''https://u.y.qq.com/cgi-bin/musicu.fcg?callback=getplaysongvkey2236996910208997&g_tk=5381&jsonpCallback=getplaysongvkey2236996910208997&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&data={"req":{"module":"CDN.SrfCdnDispatchServer","method":"GetCdnDispatch","param":{"guid":"8665097290","calltype":0,"userip":""}},"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"8665097290","songmid":["''' + \
        id+'''"],"songtype":[0],"uin":"0","loginflag":1,"platform":"20"}},"comm":{"uin":0,"format":"json","ct":20,"cv":0}}'''
    r = session.get(searchurl).text
    songjson = json.loads(r[32:-1:])
    url = songjson['req_0']['data']['sip'][0] + \
        songjson['req_0']['data']['midurlinfo'][0]['purl']
else:
    print("无效选项！")
    sys.exit(0)
if not os.path.exists("F:\\DownloadMusic"):
    os.mkdir("F:\\DownloadMusic")
with open(f"F:\\DownloadMusic\\{id}.mp3", 'wb') as ms:
    raw = session.get(url, headers={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0',
    })
    content = raw.content
    if len(content) > 500:
        ms.write(content)
        print("下载成功F:\\DownloadMusic\\{id}.mp3（不排除无效id/mid）")
    else:
        print("下载失败")
