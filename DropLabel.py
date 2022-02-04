from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtGui import QDrag, QPixmap, QPainter, QImage
from PyQt5.QtCore import QMimeData, Qt
import numpy as np
import cv2


class DraggableLabel(QLabel):
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return
        drag = QDrag(self)
        mimedata = QMimeData()
        mimedata.setText(self.text())
        drag.setMimeData(mimedata)
        pixmap = QPixmap(self.size())
        painter = QPainter(pixmap)
        painter.drawPixmap(self.rect(), self.grab())
        painter.end()
        drag.setPixmap(pixmap)
        drag.setHotSpot(event.pos())
        drag.exec_(Qt.CopyAction | Qt.MoveAction)


class DropLabel(QLabel):
    def __init__(self, *args, **kwargs):
        QLabel.__init__(self, *args, **kwargs)
        self.setAcceptDrops(True)
        self.path = None

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if len(urls) > 0:
            self.path = urls[0].toString().replace(
                'file:///', '')  # ????????
            print(self.path)
            self.show_image(self.path)
            event.acceptProposedAction()

    def show_image(self, image):
        if isinstance(image, str):
            qimage = QImage(image)
        elif isinstance(image, np.ndarray):
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            qimage = QImage(
                image, image.shape[1], image.shape[0], image.shape[1]*3, QImage.Format_RGB888)
        else:
            raise TypeError("parameter image should be str or ndarray!")
        self.setScaledContents(True)
        self.setPixmap(QPixmap.fromImage(qimage))
