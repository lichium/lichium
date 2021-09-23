'''
能不能好好说话（拼音首字母缩写补全）

指令：（拼音首字母必选，否则追问一次）
补全 <拼音首字母>
'''
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp import Message
import requests

complete_text = on_command("补全", rule=to_me(), priority=5)

@complete_text.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    if args:
        state["uncompleted_text"] = args  # 如果用户发送了参数则直接赋值

@complete_text.got("uncompleted_text", prompt="不告我缩写怎么补全呐！")
async def handle_uncompleted_text(bot: Bot, event: Event, state: T_State):
    if len(state["uncompleted_text"]) != 1:
        completed_text = await get_completed_text(state["uncompleted_text"])
        await complete_text.finish(completed_text)
    else:
        await complete_text.finish('啊呐，单个字母无法补全')

async def get_completed_text(uncompleted_text: str):
    try:
        complete_text_url_back = requests.post('https://lab.magiconch.com/api/nbnhhsh/guess/',data={'text': uncompleted_text}).json()
    except:
        return '[ERROR]请求超时'
    else:
        if complete_text_url_back:  #判断是否为空列表
            complete_text_reply=''
            try:
                complete_text_url_back[0]["trans"]=complete_text_url_back[0]['inputting']
                del(complete_text_url_back[0]['inputting'])
            except:pass
            if complete_text_url_back[0]['trans']:  #判断是否为空列表
                for _ in complete_text_url_back[0]['trans']:
                    complete_text_reply += (_ + '，')
                complete_text_reply = complete_text_reply[:-1]
                complete_text_reply = '{}的补全结果：\n{}'.format(complete_text_url_back[0]['name'],complete_text_reply)
                return complete_text_reply
            else:
                return '啊呐，无补全结果'
        else:
            return '啊呐，无补全结果'
