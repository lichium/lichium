'''
计算器（应该安全了）

不想舍弃py的位运算符，故不对括号外的运算符转义。
自动将中文括号转义为py可识别的英文括号。
加+ 减- 乘* 除/（取余数% 取整除//） 幂** 

指令：
计算 <无等号算式>
'''
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from asteval import Interpreter

calculator = on_command("计算", rule=to_me(), priority=5)
#创建安全的eval函数：极低权限
my_eval = Interpreter(use_numpy=False,minimal=False,no_if=True,no_for=True,no_while=True,no_try=True,no_functiondef=True,no_ifexp=True,no_listcomp=True,no_augassign=True,no_assert=True,no_delete=True,no_raise=True,no_print=True)

@calculator.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    if args:
        state["formula"] = args  # 如果用户发送了参数则直接赋值


@calculator.got("formula", prompt="不告我式子怎么求值呐！")
async def handle_formula(bot: Bot, event: Event, state: T_State):
    formula_value = await get_value(state["formula"])
    await calculator.finish(formula_value)

async def get_value(formula: str):
    if '=' in formula:
        return '不要包含 等号 呐！'
    else:
        formula = formula.replace('（', '(').replace('）', ')')
        return formula + '=\n' + str(my_eval(formula))