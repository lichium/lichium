'''
微软数学

指令：（式子可选，否则发送微软数学web端）
数学 [式子]
'''
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event, cqhttp

math = on_command("数学", rule=to_me(), priority=5)

@math.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    if args:
        math_reply = cqhttp.message.Message(f'[CQ:share,url=https://mathsolver.microsoft.com/zh/solve-problem/{args},title={args},content=微软数学,image=https://bingedu.azureedge.net/mathuxjs/_next/static/images/AppLogo-cd55b3354fa66ca2948db0f879dc80bd.webp]')
    else:
        math_reply = cqhttp.message.Message('[CQ:share,url=https://mathsolver.microsoft.com/zh,title=微软数学,image=https://bingedu.azureedge.net/mathuxjs/_next/static/images/AppLogo-cd55b3354fa66ca2948db0f879dc80bd.webp]')
    await math.finish(math_reply)

