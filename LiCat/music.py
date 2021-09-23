'''
搜索音乐、随机音乐（网易云音乐）

指令：（歌名可选，无歌名则返回随机音乐）
点歌 [歌名]
'''
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event, cqhttp
import requests, re

music = on_command("点歌", rule=to_me(), priority=5)

@music.handle()
async def handle_music_name(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    if args:
        music_back = await get_music(args)
    else:
        music_back = await random_music()    #否则随即音乐
    await music.finish(music_back)

async def get_music(music_name: str):
    try:
        music_back = requests.post('http://music.163.com/api/search/pc',data={'s':music_name,'offset':0,'limit':1,'type':1}).json()
    except:
        return '[ERROR]连接超时'
    else:
        if music_back['result']['songCount'] != 0:    #如果搜索到歌曲
            return cqhttp.message.Message(f"[CQ:music,type=custom,url={'https://music.163.com/#/song?id='+str(music_back['result']['songs'][0]['id'])},audio={'http://music.163.com/song/media/outer/url?id='+str(music_back['result']['songs'][0]['id'])},title={music_back['result']['songs'][0]['name']},image={music_back['result']['songs'][0]['album']['blurPicUrl']+'?param=130y130'},content={music_back['result']['songs'][0]['artists'][0]['name']}]")
        else :
            return '没有搜索到相关歌曲QAQ'

async def random_music():
    try:
        music_back = requests.get('https://api.uomg.com/api/rand.music?sort=热歌榜&format=json').json()
    except:
        return '[ERROR]连接超时'
    else:
        if music_back['code'] == 1:
            return cqhttp.message.Message(f"[CQ:music,type=custom,url={music_back['data']['url'].replace('http://music.163.com/song/media/outer/url','https://music.163.com/#/song')},audio={music_back['data']['url']},title={music_back['data']['name']},image={music_back['data']['picurl']+'?param=130y130'},content={music_back['data']['artistsname']}]")
        else:
            return '随即歌曲失败！请重试'