import os
import hashlib
import hmac
import math
import threading
import time
from urllib import parse
import requests
import json
from Crypto.Cipher import AES
from binascii import b2a_hex

# 版本控制
print('ewt360刷课工具 作者landuoguo V1.5.2.1破解版 https://github.com/landuoguo/ewt360')
account = input('输入账号: ')
password = input('输入密码: ')

# 服务降级设置，downgrade=1强制降级，downgrade=0自动降级
# 若downgrade=1异常建议手动改至downgrade=0
downgrade = 1

# 准备加密后的password


def py_aes(text):
    key = b'20171109124536982017110912453698'
    text = text.encode('utf-8')
    cryptor = AES.new(key, (AES.MODE_CBC), iv=b'2017110912453698')
    pad = 16 - len(text) % 16
    text = text + (chr(pad) * pad).encode('utf-8')
    ciphertext = cryptor.encrypt(text)
    return b2a_hex(ciphertext).decode('utf-8').upper()


def login():
    global token
    timestamp = math.floor(time.time())
    header = {'accept': 'application/json',
              'accept-language': 'zh-CN,zh;q=0.9',  'content-type': 'application/json;charset=UTF-8',  'origin': 'https://web.ewt360.com',  'platform': '1',
              'referer': 'https://web.ewt360.com/',
              'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',  'sec-ch-ua-mobile': '?0',
              'sec-ch-ua-platform': '"Windows"',  'sec-fetch-dest': 'empty',
              'sec-fetch-mode': 'cors',  'sec-fetch-site': 'same-site',  'secretid': '2',
              'sign': hashlib.md5(str(timestamp).encode('utf8') + 'bdc739ff2dcf'.encode('utf8')).hexdigest().upper(),
              'timestamp': str(timestamp),
              'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'}
    payload = {'autoLogin': 'true',
               'password': py_aes(password),
               'platform': 1,
               'userName': account}
    url = 'https://gateway.ewt360.com/api/authcenter/v2/oauth/login/account'
    try:
        Response = requests.post(url, data=json.dumps(payload), headers=header)
        data = json.loads(Response.text)
        if data['code'] == '200':
            token = data['data']['token']
        else:
            print('login ERROR')
            print(Response.text)
            raise Exception('Error 5020')
    except:
        os.system('pause')

# 获取schoolid和userid


def getuserinfo():
    global schoolid, userid
    url = 'https://teacher.ewt360.com/api/eteacherproduct/school/getSchoolUserInfo'
    header = {
        'content-type': 'text/plain', 'access-control-allow-origin': '*',
        'origin': 'https://teacher.ewt360.com', 'referer': 'https://teacher.ewt360.com/',
        'referurl': 'https://teacher.ewt360.com/ewtbend/bend/index/index.html#/holiday/student/home?sceneId=75&grade=0',
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Microsoft Edge";v="104"',
        'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-site',
        'token': token,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54',
    }
    try:
        Response = requests.get(url, headers=header)
        data = json.loads(Response.text)
        if data['code'] == '200':
            schoolid = data['data']['schoolId']
            userid = data['data']['userId']
        else:
            print('get userinfo ERROR')
            print(Response.text)
            raise Exception('Error 5001')
    except:
        os.system('pause')

# 获取sceneid


def getsceneid():
    timestamp = math.floor(time.time())
    url = 'https://gateway.ewt360.com/api/holidayprod/scene/student/study/checkHoliday?clientType=1&preview=0&schoolId=' + \
        str(schoolid) + '&timestamp=' + str(timestamp)
    header = {
        'content-type': "text/plain",  'access-control-allow-origin': "*",
        'origin': "https://teacher.ewt360.com", 'referer': "https://teacher.ewt360.com/",
        'referurl': "https://teacher.ewt360.com/ewtbend/bend/index/index.html#/holiday/student/home",
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Microsoft Edge";v="104"',
        'sec-ch-ua-mobile': "?0",  'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': "empty",  'sec-fetch-mode': "cors",  'sec-fetch-site': "same-site",
        'token': token,
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54"}
    try:
        Response = requests.get(url, headers=header)
        data = json.loads(Response.text)
        if data['code'] == '200':
            return data['data']['sceneList']
        print('get sceneid ERROR')
        print(Response.text)
        raise Exception('Error 5009')
    except:
        os.system('pause')

# 获取作业日程


def getdaylist(homeworkid, sceneid):
    url = 'https://gateway.ewt360.com/api/homeworkprod/homework/student/holiday/getHomeworkDistribution?sceneId=' + \
        str(sceneid)
    header = {
        'content-type': 'application/json',
        'origin': 'https://teacher.ewt360.com',  'referer': 'https://teacher.ewt360.com/',
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Microsoft Edge";v="104"',
        'sec-ch-ua-mobile': "?0", 'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': "empty",  'sec-fetch-mode': "cors",  'sec-fetch-site': "same-site",
        'token': token,
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54"}
    payload = {'homeworkIds': [
        homeworkid],
        'isSelfTask': 'false',
        'userOptionTaskId': 'null',  'schoolId': schoolid,
        'sceneId': str(sceneid)}
    try:
        Response = requests.post(url, data=(
            json.dumps(payload)), headers=header)
        data = json.loads(Response.text)
        if data['code'] == '200':
            return data['data']['days']
        else:
            print('get daylist ERROR')
            print(Response.text)
            raise Exception('Error 5003')
    except:
        os.system('pause')

# 获取每日作业列表


def gethomeworklist(homeworkid, daydata, sceneid):
    url = 'https://gateway.ewt360.com/api/homeworkprod/homework/student/holiday/pageHomeworkTasks?sceneId=' + \
        str(sceneid)
    header = {
        'content-type': "application/json",
        'origin': "https://teacher.ewt360.com",
        'referer': "https://teacher.ewt360.com/",
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Microsoft Edge";v="104"',
        'sec-ch-ua-mobile': "?0",  'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': "empty",  'sec-fetch-mode': "cors",  'sec-fetch-site': "same-site",
        'token': token,
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54"}
    payload = {'dayId': [
        daydata['dayId'][0]],
        'day': daydata['day'],
        'status': 0,
        'homeworkIds': [
        homeworkid],
        'isSelfTask': 'false',
        'userOptionTaskId': 'null',  'pageIndex': 1,
        'pageSize': 30,  'missionType': 0,  'schoolId': schoolid,
        'sceneId': str(sceneid)}
    try:
        Response = requests.post(url, data=(
            json.dumps(payload)), headers=header)
        data = json.loads(Response.text)
        if data['code'] == '200':
            return data['data']
        else:
            print('get homeworklist ERROR')
            print(Response.text)
            raise Exception('Error 5004')
    except:
        os.system('pause')

# 获取密钥


def getsecret(timestamp):
    global downgrade
    global secret
    global x_bfe_session_id
    header = {'token': token,
              'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54'}
    url = 'https://bfe.ewt360.com/monitor/hmacSecret?userId=' + \
        str(userid) + '&_=' + str(timestamp)
    try:
        Response = requests.get(url, headers=header)
        json2 = json.loads(Response.text)
        if json2['code'] == 200:
            secret = json2['data']['secret']
            x_bfe_session_id = json2['data']['sessionId']
        elif (json2['code'] == 699999):
            downgrade = 1
        else:
            print('get secret ERROR')
            print(Response.text)
            raise Exception('Error 5005')
    except:
        os.system('pause')


def uploadprogress_clog(timestamp, duration, begin_time, lesson_id, course_id, day, cls, i):
    header = {
        'Accept': "*/*",  'Accept-Encoding': "gzip, deflate, br",
        'Accept-Language': "zh-CN,zh;q=0.9",  'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
        'Host': "clog.ewt360.com",  'Origin': "https://web.ewt360.com",
        'Referer': "https://web.ewt360.com/",  'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Microsoft Edge";v="104"',
        'sec-ch-ua-mobile': "?0",  'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Dest': "empty",  'Sec-Fetch-Mode': "cors",  'Sec-Fetch-Site': "same-site",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 Edg/104.0.1293.63"}
    content = {'CommonPackage': {
        'version': "1.0",
        'userid': userid,
        'ip': "",  'os': "Win32", 'os_bit': "32-bit",  'resolution': "1920*1080",
        'mstid': token,
        'browser': "Chrome",
        'browser_ver': "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 Edg/104.0.1293.63",
        'playerType': 1,  'sdkVersion': "1.0.0"},
        'EventPackage': [
        {
            'lesson_id': lesson_id,
            'course_id': course_id,
            'stay_time': duration,
            'status': 1,
            'begin_time': begin_time,
            'report_time': timestamp,
            'point_time_id': 0,
            'point_time': "60000",
            'point_num': "19",  'video_type': 1,
            'speed': 1,  'quality': "1",
            'video_index': ""}]}
    try:
        url = 'https://clog.ewt360.com/?sn=ewt_web_video_detail&log='
        url += parse.quote(json.dumps(content))
        url += '&ts=' + str(timestamp)
        Response = requests.get(url, headers=header)
        if Response.status_code == 200:
            print('day:' + str(day['day']) + ',name:' +
                  str(cls['title']) + ' #' + str(i) + ' OK(clog)')
        else:
            print('upload progress(clog) ERROR')
            print(Response.headers)
            raise Exception('Error 5010')
    except:
        pass
# 上传进度


def uploadprogress(signature, lesson_id, course_id, timestamp, duration, begin_time, day, cls, i):
    url = 'https://bfe.ewt360.com/monitor/web/collect/batch?_=' + \
        str(timestamp)
    header = {
        'access-control-allow-origin': "*",
        'content-type': "application/json",
        'origin': "https://web.ewt360.com",
        'referer': "https://web.ewt360.com/",
        'sec-ch-ua-mobile': "?0",
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': "empty",
        'sec-fetch-mode': "cors",
        'sec-fetch-site': "same-site",
        'token': token,
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.80 Safari/537.36 Edg/104.0.1293.52",
        'x-bfe-session-id': 'x_bfe_session_id'}
    payload = {'CommonPackage': {
        'version': "1.0",  'userid': userid,
        'ip': "",  'os': "Win32",  'os_bit': "32-bit",  'resolution': "1920*1080",
        'mstid': token,
        'browser': "Chrome",  'browser_ver': "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54",
        'playerType': 1,  'sdkVersion': "1.0.0"},
        'EventPackage': [
        {
            'lesson_id': lesson_id,
            'course_id': course_id,
            'stay_time': duration,
            'status': 1,
            'begin_time': begin_time,
            'report_time': timestamp,
            'point_time_id': 0,
            'point_time': 60000,
            'point_num': 11,
            'video_type': 1,
            'speed': 2,
            'quality': "1",
            'video_index': "",
            'action': action}],
        'signature': signature,
        'sn': 'ewt_web_video_detail'}
    try:
        # Response = requests.post(url)
        Response = requests.post(url, data=(
            json.dumps(payload)), headers=header)
        json2 = json.loads(Response.text)
        if json2['code'] == '200':
            print('day:' + str(day['day']) + ',name:' +
                  str(cls['title']) + ' #' + str(i) + ' OK')
        else:
            print('upload progress ERROR')
            print(Response.text)
            raise Exception('Error 5011')
    except:
        os.system('pause')


def gethomeworkid(sceneid):
    timestamp = math.floor(time.time())
    url = 'https://gateway.ewt360.com/api/homeworkprod/homework/student/holiday/getHomeworkSummaryInfo?schoolId=' + \
        str(schoolid) + '&timestamp=' + \
        str(timestamp) + '&sceneId=' + str(sceneid)
    header = {
        'content-type': 'text/plain', 'access-control-allow-origin': '*',
        'origin': 'https://teacher.ewt360.com', 'referer': 'https://teacher.ewt360.com/',
        'referurl': 'https://teacher.ewt360.com/ewtbend/bend/index/index.html#/holiday/student/home?sceneId=75&grade=0',
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Microsoft Edge";v="104"',
        'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-site',
        'token': token,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54',
    }
    try:
        Response = requests.get(url, headers=header)
        data = json.loads(Response.text)
        if data['code'] == '200':
            return data['data']['homeworkIds']
        else:
            print('get homeworkid ERROR')
            print(Response.text)
            raise Exception('Error 5003')
    except:
        os.system('pause')


# 主函数
if __name__ == '__main__':
    login()
    getuserinfo()
    sc = getsceneid()
    sceneid = sc[0]['id']
    input('准备工作完成，回车开始学习，ctrl+c退出！')
    for ho in gethomeworkid(sceneid):
        for day in getdaylist(ho, sceneid):
            homeworklist = gethomeworklist(ho, day, sceneid)
            if homeworklist['totalRecords'] == 0:
                continue
            for cls in homeworklist['data']:
                if cls['contentType'] != 1:
                    continue
                lesson_id = cls['contentId']
                course_id = cls['parentContentId']
                timestamp = math.floor(time.time())
                if downgrade == 0:  # 自动
                    getsecret(timestamp)
                    for i in range(0, 30):
                        begin_time = math.floor(time.time()) - 100000
                        timestamp = math.floor(time.time())
                        duration = timestamp - begin_time
                        action = 2
                        hmacmsg = 'action=' + str(action) + '&duration=' + str(duration) + '&mstid=' + str(
                            token) + '&signatureMethod=HMAC-SHA1&signatureVersion=1.0&timestamp=' + str(timestamp) + '&version=2022-08-02'
                        signature = hmac.new(bytes(
                            secret, encoding='utf-8'), hmacmsg.encode('utf-8'), hashlib.sha1).hexdigest()
                        threading.Thread(target=uploadprogress, args=(
                            signature, lesson_id, course_id, timestamp, duration, begin_time, day, cls, i)).start()
                        time.sleep(3)
                elif downgrade == 1:  # 强制√
                    for i in range(0, 30):
                        begin_time = math.floor(time.time()) - 100000
                        timestamp = math.floor(time.time())
                        duration = timestamp - begin_time
                        threading.Thread(target=uploadprogress_clog, args=(
                            timestamp, duration, begin_time, lesson_id, course_id, day, cls, i)).start()
                        time.sleep(0.1)
                else:
                    time.sleep(0.05)
            cmd = input('已学完一天课程，是否继续？继续请输入1，退出请输入0：')
            if cmd == '1':
                continue
            elif cmd == '0':
                os._exit()
            else:
                print('错误的输入，回车后退出程序。')
                input()
                os._exit()

    time.sleep(2)
    print('全部学习完毕！')
    os.system('pause')
