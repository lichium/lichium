'''
作品名：信条
作者：Limpu

版本：1
最后修改：2021年5月1日

下载说明：
    图片和程序下载后保存在D:\\xt
    才可正常运行（呜呜呜不会打包）

使用说明：
    启动程序将在屏幕右下角出现一个窗口,
    窗口获取焦点时按“Tab”截图，保存至桌面，
    输入框空时按按钮获取“一言”，显示并朗读，
    输入框不为空时按按钮返回ai回复，显示并朗读，
    按Alt+F4关闭窗口。
'''


from tkinter import *
import json
import os
import re
import time

import pyautogui
import pyttsx3
import requests


global aiinput

class tool:
    def __init__(self):
        global times
        times = True
        global working
        working = False
        global person_gif
        person_gif = PhotoImage(file='D:\\xt\\person.gif')#人物载入程序

    def say(self,text):#显示消息
        txt = Label(xt,text=text,font=('楷体',12),bg='linen',wrap=120)
        txt.place(x=0,y=0,width=120,height=100)
        reader.say(text)
    
    def sentence(self):#获取佳句
        sentence = requests.get('https://v1.hitokoto.cn/?max_length=45').json()
        sentence = sentence['hitokoto']
        return sentence

    def keyboardevent(self,event):#键盘事件
        if event.keycode == 9:#按‘Tab’截图（焦点须在窗口）
            screen = pyautogui.screenshot()
            #查找保存路径
            path='C:\\Users\\Admin\\Desktop\\creen.png'
            directory, file_name = os.path.split(path)
            while os.path.isfile(path):
                pattern = '(\d+)\)\.'
                if re.search(pattern, file_name) is None:
                    file_name = file_name.replace('.', '(0).')
                else:
                    current_number = int(re.findall(pattern, file_name)[-1])
                    new_number = current_number + 1
                    file_name = file_name.replace(f'({current_number}).', f'({new_number}).')
                path = os.path.join(directory + os.sep + file_name)
            screen.save(path)#保存

    def do(self):
        global aiinput
        global working
        if not working:
            working = True
            text = str(aiinput.get())
            aiinput.delete(0, END)
            if text == '':
                tool.say(tool.sentence())
                xt.after(100,tool.domore)
            else:
                back = requests.get('http://api.qingyunke.com/api.php?key=free&appid=0&msg='+text).json()['content']
                tool.say(back)
                xt.after(100,tool.domore)
    def domore(self):
        reader.runAndWait()
        time.sleep(1)
        global working
        working = False
        tool.main()
    
    def main(self):
        person_img = Label(xt, image = person_gif)  
        person_img.place(x=0,y=0)
        
        global aiinput
        global times
        if times:
            v = StringVar(xt, value='Alt+F4关闭窗口')
            aiinput = Entry(xt,textvariable=v)
            aiinput.place(x=0,y=100,width=100,height=20)
            times = False
        else:
            aiinput = Entry(xt)
            aiinput.place(x=0,y=100,width=100,height=20)

        aibutton = Button(xt,text='⏎',command = tool.do)
        aibutton.place(x=100,y=100,width=20,height=20)


#初始化窗口xt
xt = Tk()
xt.title('TENET')
xt.geometry('120x120-0-41')
xt.resizable(False, False)
xt.wm_attributes('-topmost',True,'-alpha', 0.9)
xt.overrideredirect(True)
xt.configure(bg='')

tool = tool()#实例化所有工具
reader = pyttsx3.init()#实例化朗读者
xt.bind("<KeyRelease>",tool.keyboardevent)#绑定任意键（截图）

#主程序
tool.main()

xt.mainloop()#进入循环
