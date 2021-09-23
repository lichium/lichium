'''
天气查询（现在、今天、明天）

指令：（城市必选，否则追问一次）
天气 <城市>
'''
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
import requests

weather = on_command("天气", rule=to_me(), priority=5)

@weather.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
    if args:
        state["city"] = args  # 如果用户发送了参数则直接赋值


@weather.got("city", prompt="不告我位置怎么查天气呐！")
async def handle_city(bot: Bot, event: Event, state: T_State):
    city_weather = await get_weather(state["city"])
    await weather.finish(city_weather)

async def get_weather(city: str):
    try:
        weather_url_back = requests.get('https://api2.jirengu.com/getWeather.php?city='+city,timeout=1).json()
    except:
        return '[ERROR]请求超时'
    else:
        if weather_url_back["message"] == 'success':
            weather_url_back = '{}现在天气：\n{}，{}℃，湿度{}%，{}{}\n今天天气：\n{}/{}，{}~{}℃，{}{}/{}{}\n明天天气：\n{}/{}，{}~{}℃，{}{}/{}{}'\
                .format(weather_url_back["result"]["location"]["name"],weather_url_back["result"]["now"]["text"],weather_url_back["result"]["now"]["temp"],\
                weather_url_back["result"]["now"]["rh"],weather_url_back["result"]["now"]["wind_dir"],weather_url_back["result"]["now"]["wind_class"],\
                weather_url_back["result"]["forecasts"][0]["text_day"],weather_url_back["result"]["forecasts"][0]["text_night"],\
                weather_url_back["result"]["forecasts"][0]["low"],weather_url_back["result"]["forecasts"][0]["high"],weather_url_back["result"]["forecasts"][0]["wd_day"],\
                weather_url_back["result"]["forecasts"][0]["wc_day"],weather_url_back["result"]["forecasts"][0]["wd_night"],weather_url_back["result"]["forecasts"][0]["wc_night"],\
                weather_url_back["result"]["forecasts"][1]["text_day"],weather_url_back["result"]["forecasts"][1]["text_night"],\
                weather_url_back["result"]["forecasts"][1]["low"],weather_url_back["result"]["forecasts"][1]["high"],weather_url_back["result"]["forecasts"][1]["wd_day"],\
                weather_url_back["result"]["forecasts"][1]["wc_day"],weather_url_back["result"]["forecasts"][1]["wd_night"],weather_url_back["result"]["forecasts"][1]["wc_night"])
            return weather_url_back
        else:
            return '查询失败，请检查拼写'