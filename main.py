import requests
import sys
from geocoder import get_coordinates
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class MainWindow(QWidget):
    def __init__(self, parent=None):
        self.map_ll = [37.977751, 55.757718]
        self.map_l = 0
        self.map_zoom = 5
        self.map_size = (600, 400)
        self.delta_arrows = 0.1
        self.modes = ["map", "sat", "sat,skl"]
        self.geocoder_apikey = "40d1649f-0493-4b70-98ba-98533de7710b"
        # метки
        self.pt = []

        super(MainWindow, self).__init__(parent)
        self.loadUI()
        self.resize(600, 450)
        self.setWindowTitle('YAPet')
        self.show()
        self.refresh()
        self.start_search_button.clicked.connect(self.find_object)

    def switch_mode(self):
        self.map_l = (self.map_l + 1) % len(self.modes)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Tab:
            self.switch_mode()

        if event.key() == Qt.Key_PageUp and self.map_zoom < 18:
            self.map_zoom += 1

        if event.key() == Qt.Key_PageDown and self.map_zoom > 0:
            self.map_zoom -= 1

        # стрелки
        if event.key() == Qt.Key_Left:
            self.map_ll[0] -= self.delta_arrows

        if event.key() == Qt.Key_Right:
            self.map_ll[0] += self.delta_arrows

        if event.key() == Qt.Key_Up:
            self.map_ll[1] += self.delta_arrows

        if event.key() == Qt.Key_Down:
            self.map_ll[1] -= self.delta_arrows

        # нажимаем на кнопку F1 и "выключаем" текстовое поле
        # чтобы стрелки right/left работали корректно
        if event.key() == Qt.Key_F1:
            self.search_field.setEnabled(not self.search_field.isEnabled())
            self.start_search_button.setEnabled(not self.start_search_button.isEnabled())

        self.refresh()

    def find_object(self):
        response_text = self.search_field.text()
        coordinates = get_coordinates(response_text)

        if not coordinates:
            return

        self.pt.append("{},{},vkbkm".format(*coordinates))
        self.map_ll = list(coordinates)

        self.refresh()

    def refresh(self):
        params = {
            "ll": ','.join(map(str, self.map_ll)),
            "l": self.modes[self.map_l],
            'z': self.map_zoom,
            "size": ','.join(map(str, self.map_size))
        }
        if self.pt:
            params["pt"] = '~'.join(self.pt)

        response = requests.get('https://static-maps.yandex.ru/1.x/', params=params)
        pixmap = QPixmap()
        pixmap.loadFromData(response.content)
        self.label.setPixmap(pixmap)

    def loadUI(self):
        self.label = QLabel(self)
        self.label.move(0, 50)
        self.label.resize(*self.map_size)

        # запрос
        self.search_field = QLineEdit(self)
        self.search_field.move(3, 3)
        self.search_field.resize(505, 40)
        self.search_field.setEnabled(False)

        # кнопка искать
        self.start_search_button = QPushButton(self)
        self.start_search_button.move(511, 3)
        self.start_search_button.resize(87, 40)
        self.start_search_button.setText("Искать")
        self.start_search_button.setEnabled(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
