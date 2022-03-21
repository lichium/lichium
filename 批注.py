'''
《批注》
最后更改：2022-3-21
作者：Limpu

起因：我班老师困扰于电脑自带批注功能无法被录制、PPT批注难以使用、某不知名教学软件的批注功能操作不
    便利的问题，多次报修无果，大悲，作此程序。
简介：运行程序，在屏幕左侧偏下生成一个小窗口，勾选第一个开关即开启批注，你可以在屏幕上乱画，RBG按
    钮为别为红蓝绿色画笔。实现原理是在屏幕上置顶一个背景不透明度为1的窗口。

借鉴：https://www.cnblogs.com/PyLearn/p/7689170.html
一切开发旨在学习用途，禁用于非法用途，不鼓励用于商业用途，侵权请联系删除
windows下测试正常，高性能。
'''
from sys import argv
from PyQt5.QtWidgets import (QApplication, QWidget, QRadioButton, QPushButton, QLineEdit)
from PyQt5.QtGui import (QPainter, QPen, QColor)
from PyQt5.QtCore import Qt


class Example(QWidget):
    def __init__(self):
        global pos_xy
        super(Example, self).__init__()
        # resize设置宽高，move设置位置
        self.resize(screenSizeX-15, screenSizeY)
        self.move(15, 0)
        self.setWindowTitle("批注")
        self.setMouseTracking(False)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint |
                            Qt.WindowType.SplashScreen | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        pos_xy = []

    def paintEvent(self, event):
        global penSize
        painter = QPainter()
        painter.begin(self)
        painter.fillRect(0, 0, self.width(),
                         self.height(), QColor(0, 0, 0, 1))
        if len(pos_xy) > 1:
            point_start = pos_xy[0]
            for pos_tmp in pos_xy:
                point_end = pos_tmp
                if point_end == (-1, -1, 0):
                    point_start = (-1, -1, 0)
                    continue
                if point_start == (-1, -1, 0):
                    point_start = point_end
                    continue
                painter.setPen(QPen(point_start[2], penSize, Qt.SolidLine))
                painter.drawLine(
                    point_start[0], point_start[1], point_end[0], point_end[1])
                point_start = point_end
        painter.end()

    def mouseMoveEvent(self, event):
        global colour
        # 中间变量pos_tmp提取当前点
        pos_tmp = (event.pos().x(), event.pos().y(), colour)
        # pos_tmp添加到self.pos_xy中
        pos_xy.append(pos_tmp)
        self.update()

    def mouseReleaseEvent(self, event):
        pos_test = (-1, -1, 0)
        pos_xy.append(pos_test)
        self.update()


class Trigger(QWidget):
    def __init__(self):
        super(Trigger, self).__init__()
        self.setWindowFlags(Qt.Tool)
        self.resize(15, 88)
        self.move(0, screenSizeY-200)
        self.setWindowTitle("批注开关")
        self.setMouseTracking(False)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint |
                            Qt.WindowType.SplashScreen | Qt.WindowType.WindowStaysOnTopHint)
        self.button = QRadioButton('', self)
        self.button.resize(15, 15)
        self.button.toggled.connect(self.switch)
        self.r = QPushButton('R', self)
        self.r.resize(15, 20)
        self.r.move(0, 13)
        self.r.clicked.connect(lambda: self.setColour(Qt.red))
        self.b = QPushButton('B', self)
        self.b.resize(15, 20)
        self.b.move(0, 33)
        self.b.clicked.connect(lambda: self.setColour(Qt.blue))
        self.g = QPushButton('G', self)
        self.g.resize(15, 20)
        self.g.move(0, 53)
        self.g.clicked.connect(lambda: self.setColour(Qt.darkGreen))
        self.input = QLineEdit(self)
        self.input.resize(15,15)
        self.input.move(0,73)
        self.input.textChanged.connect(self.setSize)

    def switch(self):
        global pos_xy
        if self.button.isChecked():
            main.show()
        else:
            main.close()
            del(pos_xy)
            pos_xy = []

    def setColour(self, c):
        global colour
        colour = c
    
    def setSize(self, text):
        global penSize
        try:
            penSize = int(text)
        except:
            penSize = 2

if __name__ == "__main__":
    colour, penSize = Qt.red, 2
    app = QApplication(argv)
    screenSizeX, screenSizeY = app.desktop().width(), app.desktop().height()
    main = Example()
    trigger = Trigger()
    trigger.show()
    app.exec_()
