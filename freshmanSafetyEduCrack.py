import requests

print("*"*100)
userId=input("请输入用户ID：")

while True:
    print("*"*100)
    articleId=int(input("请输入章节ID（知识页网址中id字段）："))


    get_questionIDlist_url = 'http://wap.xiaoyuananquantong.com/guns-vip-main/wap/question/list?articleId={}&ah='.format(articleId)
    questionIDlist = requests.get(get_questionIDlist_url).json()

    fakeAswer = [("articleId",articleId),("userId",userId),("ah","")]

    type_map={"单选":1,"多选":2,"判断":3}

    for i in questionIDlist["data"]["list"]:
        type = type_map[i["quesType"]]
        if type==1:
            fakeAswer.extend([("question","{}-X".format(i["id"])),("quesType","1")])
        elif type==2:
            fakeAswer.extend([("question","~{}-X".format(i["id"])),("quesType","2")])
        elif type==3:
            fakeAswer.extend([("question","{}-2".format(i["id"])),("quesType","3")])
        else:
            print("错误1")

    re_fake = requests.post("http://wap.xiaoyuananquantong.com/guns-vip-main/wap/unitTest",data=fakeAswer).json()


    logId = int(re_fake["data"]["logId"])

    get_realAnswer_url = 'http://wap.xiaoyuananquantong.com/guns-vip-main/wap/wrong/list?errorLogId={}&page=1&limit=999'.format(logId)
    realAnswer = requests.get(get_realAnswer_url).json()

    postRealAswer=[("articleId",articleId),("userId",userId),("ah","")]

    for j in realAnswer["data"]["data"]:
        type = int(j["question"]["quesType"])
        if type==1:
            postRealAswer.extend([("question","{}-{}".format(j["questionId"],j["question"]["answer"])),("quesType","1")])
        elif type==2:
            multiAnswerList = j["question"]["answer"].split(",")
            postMultiAnswer = ""
            for k in multiAnswerList:
                if k!="":
                    postMultiAnswer += "~{}-{}".format(j["questionId"],k)
            postRealAswer.extend([("question",postMultiAnswer),("quesType","2")])

        elif type==3:
            postRealAswer.extend([("question","{}-{}".format(j["questionId"],j["question"]["answer"])),("quesType","3")])
        else:
            print("错误2")
    re_real = requests.post("http://wap.xiaoyuananquantong.com/guns-vip-main/wap/unitTest",data=postRealAswer).json()
    if re_real["code"]==200:
        print("成功")
    else:
        print("失败")
