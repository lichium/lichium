import pcqq,requests
bot = pcqq.QQBot(adminUsers=[])

class Weather(pcqq.Plugin): #天气
    def match(self):
        return self.on_common_match('天气','不告我位置怎么查天气呐！')
    def handle(self):
        try:
            weather_url_back = requests.get('https://api2.jirengu.com/getWeather.php?city='+self.Args[-1],timeout=1).json()
        except:
            self.send_msg('[ERROR]请求超时')
        else:
            if weather_url_back["message"] == 'success':
                weather_url_back = '{}现在天气：\n{}，{}℃，湿度{}%，{}{}\n明天天气：\n{}/{}，{}~{}℃，{}{}/{}{}'\
                    .format(weather_url_back["result"]["location"]["name"],weather_url_back["result"]["now"]["text"],weather_url_back["result"]["now"]["temp"],\
                    weather_url_back["result"]["now"]["rh"],weather_url_back["result"]["now"]["wind_dir"],weather_url_back["result"]["now"]["wind_class"],\
                    weather_url_back["result"]["forecasts"][1]["text_day"],weather_url_back["result"]["forecasts"][1]["text_night"],\
                    weather_url_back["result"]["forecasts"][1]["low"],weather_url_back["result"]["forecasts"][1]["high"],weather_url_back["result"]["forecasts"][1]["wd_day"],\
                    weather_url_back["result"]["forecasts"][1]["wc_day"],weather_url_back["result"]["forecasts"][1]["wd_night"],weather_url_back["result"]["forecasts"][1]["wc_night"])
                self.send_msg(weather_url_back)
            else:
                self.send_msg('查询失败，请检查拼写')

class Complete_text(pcqq.Plugin):   #补全（能不能好好说话）
    def match(self):
        return self.on_common_match('补全','不告我内容怎么补全呐！')
    def handle(self):
        try:
            complete_text_url_back = requests.post('https://lab.magiconch.com/api/nbnhhsh/guess/',data={'text': self.Args[-1]}).json()
        except:
            self.send_msg('[ERROR]请求超时')
        else:
            if complete_text_url_back:  #判断是否为空列表
                complete_text_reply=''
                for _ in complete_text_url_back[0]['trans']:
                    complete_text_reply += (_ + '，')
                complete_text_reply += '\b\b'
                complete_text_reply = '{}的补全结果：\n{}'.format(complete_text_url_back[0]['name'],complete_text_reply)
                self.send_msg(complete_text_reply)
            else:
                self.send_msg('啊呐，无补全结果')
                
bot.RunBot()
