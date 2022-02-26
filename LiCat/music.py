'''
点歌 [歌名]

歌名可选，不填为随机
'''
from nonebot import on_command
from nonebot.log import logger
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import CommandArg

import re,httpx

music = on_command("点歌", rule=to_me(), priority=5)

@music.handle()
async def handle(matcher: Matcher, args: Message = CommandArg()):
    args = str(args).strip()
    if args =='':
        id = await random_music()
    else:
        id = await search_music(args)
    if id == '':
        msg='[ERROR]'
    else:
        msg={'type':'music','data':{'type':'163','id':id}}
    await music.finish(msg)
    
async def search_music(song_name:str) ->str:
    head={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.78"}
    para={'s':song_name,'type':1}
    api='https://music.163.com/api/search/get/web'
    async with httpx.AsyncClient() as client:
        try:
            back=await client.get(url=api,params=para,headers=head)
        except:
            logger.error('music.163.com访问超时')
            return ''
    if back.status_code!=200:
        logger.error('music.163.com状态码错误')
        return ''
    data=back.json()
    if data['result']['songCount']==0:
        return ''
    return str(data['result']['songs'][0]['id'])

async def random_music() ->str:
    api='https://api.uomg.com/api/rand.music?format=json'
    async with httpx.AsyncClient() as client:
        try:
            back=await client.get(url=api)
        except:
            logger.error('api.uomg.com访问超时')
            return ''
    if back.status_code != 200:
        logger.error('api.uomg.com状态码错误')
        return ''
    data=back.json()
    if data['code']!=1:
        return ''
    return str(re.search('(?<=\?id=)\d+',data['data']['url']).group(0))
