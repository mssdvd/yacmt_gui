import sys

import requests
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import (QApplication, QComboBox, QGridLayout, QHBoxLayout,
                             QLabel, QLCDNumber, QMainWindow, QPushButton,
                             QWidget)


class YACMT(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.lcdSpeed = QLCDNumber()
        grid.addWidget(self.lcdSpeed)
        self.lcdRPM = QLCDNumber()
        grid.addWidget(self.lcdRPM)

        self.timer = QTimer()
        self.timer.timeout.connect(self._update)
        self.timer.start(1000)

        self.setLayout(grid)
        self.setGeometry(0, 0, 320, 240)
        self.setWindowTitle('YACMT')
        self.show()

    def _update(self):
        yacm_json = requests.get("http://localhost:8080").json()
        self.lcdRPM.display(yacm_json.get("eng_rpm"))
        self.lcdSpeed.display(yacm_json.get("speed"))


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = YACMT()
    sys.exit(app.exec_())
