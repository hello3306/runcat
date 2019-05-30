"""
 Hello 

"""
import sys
import threading
import time

import psutil
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QSystemTrayIcon, QApplication, QMenu, QAction
# 静态资源的导入
from img import image
from threading import Timer
from PIL import ImageGrab


class Tary():

    def run(self):
        self.setUi()

    # 设置程序的信息
    def setUi(self):
        app = QApplication(sys.argv)
        app.setQuitOnLastWindowClosed(False)
        self.tray = QSystemTrayIcon()
        from PyQt5.QtGui import QIcon

        # 设置程序任务栏图标
        self.tray.setIcon(QIcon(':/img/0.png'))
        # 是否在任务栏显示
        self.tray.setVisible(True)

        # 设置任务栏程序的菜单
        self.menu = QMenu()

        self.quitAction = QAction()
        self.quitAction.setText('退出')
        self.quitAction.setIcon(QIcon(':/img/tc.ico'))

        self.setting = QAction()
        self.setting.setText("设置")
        self.setting.setIcon(QIcon(':/img/setting.ico'))

        self.mainWin = QAction()
        self.mainWin.setText("主页")
        self.mainWin.setIcon(QIcon(':/img/main.ico'))

        self.menu.addAction(self.mainWin)
        self.menu.addAction(self.setting)
        self.menu.addAction(self.quitAction)

        self.tray.setContextMenu(self.menu)
        self.quitAction.triggered.connect(self.quit)

        # 调用进程
        self.t()

        sys.exit(app.exec_())

    def t(self):
        self.thread = RunThread(self.tray)
        self.thread.start()

    def quit(self):
        # "保险起见，为了完整的退出"
        self.tray.setVisible(False)
        # self.tray.parent().exit()
        #  qApp.quit()
        sys.exit()


class RunThread(QThread):

    def __init__(self, tray):
        super(RunThread, self).__init__()
        self.tray = tray

    def run(self):
        self.cpurun()

    def dtime(self):
        t = Timer(3, self.img)
        t.start()

    def img(self):
        time_now = time.strftime('%Y%m%d-%H%M%S')
        pic = ImageGrab.grab()
        pic_name = time_now + '.jpg'
        pic.save(pic_name)

    # CPU和内存的计算
    def cpurun(self):
        self.cpu = 0.1
        self.mem = 0.1
        timer = threading.Timer(1, self.cpufunc, [])
        timer.start()
        while True:
            t = (self.cpu * self.cpu - 10 * self.cpu + 10) / 50
            self.dtime()
            if self.cpu * 100 > 90:
                self.tray.showMessage('新消息', '主人CPU快跑不动了')
                time.sleep(1)
            for i in range(5):
                self.tray.setIcon(QIcon(':/img/{}.png'.format(i)))
                self.tray.setToolTip('cat：' + '\r\n' +
                                     'CPU: {:.2%}'.format(self.cpu) +
                                     '\r\n'
                                     '内存: {:.2%}'.format(self.mem))
                time.sleep(t)

    # 获取CPU和内存的信息
    def cpufunc(self):
        while True:
            self.cpu = psutil.cpu_percent(interval=1) / 100
            self.mem = psutil.virtual_memory().percent / 100
            time.sleep(1)


if __name__ == "__main__":
    cat = Tary()
    cat.run()
