import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QRadioButton, QPushButton)
from PyQt5.QtGui import (QPainter, QPen, QColor)
from PyQt5.QtCore import Qt


class Example(QWidget):
    def __init__(self):
        global pos_xy
        super(Example, self).__init__()
        # resize设置宽高，move设置位置
        self.size = QApplication.desktop()
        self.resize(self.size.width()-15, int(self.size.height()*0.96))
        self.move(15, 0)
        self.setWindowTitle("批注")
        self.setMouseTracking(False)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint |
                            Qt.WindowType.SplashScreen | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        pos_xy = []

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.fillRect(0, 0, self.size.width(), int(
            self.size.height()*0.96), QColor(0, 0, 0, 1))
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
                painter.setPen(QPen(point_start[2], 2, Qt.SolidLine))
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
        self.sizey = QApplication.desktop().height()
        self.resize(15, 73)
        self.move(0, self.sizey-200)
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


if __name__ == "__main__":
    colour = Qt.red
    app = QApplication(sys.argv)
    main = Example()
    trigger = Trigger()
    trigger.show()
    app.exec_()
