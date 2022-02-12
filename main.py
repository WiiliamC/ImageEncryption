# -*- coding:gbk -*-
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from numpy import ndarray
from encryptor import encrypt, encrypt_image_by_key
from transition import percent_func_gen
import os
import cv2
import threading

UI_PATH = "encrypt.ui"


class MainWindow(QWidget):
    image_show_signal = pyqtSignal(ndarray)
    set_arrow_cursor_signal = pyqtSignal()
    set_wait_cursor_signal = pyqtSignal()

    def __init__(self):
        super(MainWindow, self).__init__()
        # 加载UI
        self.main_win = uic.loadUi(UI_PATH)
        # 连接按钮信号
        self.main_win.pushButton.clicked.connect(self.encrypt)
        self.image_show_signal.connect(self.image_show)
        self.set_arrow_cursor_signal.connect(self.set_arrow_cursor)
        self.set_wait_cursor_signal.connect(self.set_wait_cursor)
        self.main_win.lineEdit.returnPressed.connect(self.encrypt)

    def encrypt(self):
        def run():
            image_path = self.main_win.label.path
            key = self.main_win.lineEdit.text()
            if image_path is not None and len(key) != 0:
                self.set_wait_cursor_signal.emit()
                # encrypt the image
                image0 = cv2.imread(image_path)
                image1 = encrypt_image_by_key(image_path, key)
                # save the image-code
                image_folder, image_name = os.path.split(image_path)
                name, ext = os.path.splitext(image_name)
                if ext != ".bmp":
                    save_path = os.path.join(image_folder, name+".bmp")
                else:
                    save_path = os.path.join(image_folder, name+"_.bmp")
                cv2.imwrite(save_path, image1)
                # show the image
                load_f = 20
                tim = 0.3
                percent_func1 = percent_func_gen(
                    a=1, b=0, time=tim, n=1, mode="null")
                percent_func2 = percent_func_gen(
                    a=0, b=1, time=tim, n=1, mode="null")
                for t in range(int(tim * 1000) // load_f + 1):
                    percent = percent_func1(t * load_f / 1000)
                    img_show = cv2.multiply(
                        image0, (1, 1, 1, 1), scale=percent)
                    self.image_show_signal.emit(img_show)
                    cv2.waitKey(load_f)
                for t in range(int(tim * 1000) // load_f + 1):
                    percent = percent_func2(t * load_f / 1000)
                    img_show = cv2.multiply(
                        image1, (1, 1, 1, 1), scale=percent)
                    self.image_show_signal.emit(img_show)
                    cv2.waitKey(load_f)
                self.set_arrow_cursor_signal.emit()

        threading.Thread(target=run).start()

    @pyqtSlot(ndarray)
    def image_show(self, image):
        self.main_win.label.show_image(image)

    @pyqtSlot()
    def set_arrow_cursor(self):
        self.main_win.setCursor(Qt.ArrowCursor)

    @pyqtSlot()
    def set_wait_cursor(self):
        self.main_win.setCursor(Qt.WaitCursor)


if __name__ == '__main__':
    app = QApplication([])
    main = MainWindow()
    main.main_win.show()
    app.exec_()
