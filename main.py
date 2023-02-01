import requests
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class MainWindow(QWidget):
    def __init__(self, parent=None):
        self.map_ll = [37.977751, 55.757718]
        self.map_l = "map"
        self.map_zoom = 5

        super(MainWindow, self).__init__(parent)
        self.loadUI()
        self.resize(600, 450)
        self.setWindowTitle('YAPet')
        self.show()
        self.refresh()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp and self.map_zoom < 18:
            self.map_zoom += 1

        if event.key() == Qt.Key_PageDown and self.map_zoom > 0:
            self.map_zoom -= 1

        self.refresh()

    def refresh(self):
        params = {
            "ll": ','.join(map(str, self.map_ll)),
            "l": self.map_l,
            'z': self.map_zoom
        }
        response = requests.get('https://static-maps.yandex.ru/1.x/', params=params)
        with open('pic.png', 'wb') as pic:
            pic.write(response.content)

        pixmap = QPixmap()
        pixmap.load('pic.png')
        self.label.setPixmap(pixmap)

    def loadUI(self):
        self.label = QLabel(self)
        self.label.resize(600, 450)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
