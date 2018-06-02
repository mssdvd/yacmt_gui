import sys

import requests
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import (QApplication, QComboBox, QGridLayout, QHBoxLayout,
                             QLabel, QLCDNumber, QMainWindow, QPushButton,
                             QWidget)

from db import init_db, insert_report


class YACMT(QWidget):
    def __init__(self):
        super().__init__()
        init_db()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.lcdSpeed = QLCDNumber()
        grid.addWidget(self.lcdSpeed)
        self.lcdRPM = QLCDNumber()
        grid.addWidget(self.lcdRPM)

        self.display_timer = QTimer()
        self.display_timer.timeout.connect(self._update_display)
        self.display_timer.start(1000)

        self.report_timer = QTimer()
        self.report_timer.timeout.connect(self._new_report)
        self.report_timer.start(5000)

        self.setLayout(grid)
        self.setGeometry(0, 0, 320, 240)
        self.setWindowTitle('YACMT')
        self.show()

    def _update_display(self):
        yacm_json = requests.get("http://localhost:8080").json()
        self.lcdRPM.display(yacm_json.get("eng_rpm"))
        self.lcdSpeed.display(yacm_json.get("speed"))

    def _new_report(self):
        yacm_json = requests.get("http://localhost:8080").json()
        insert_report(yacm_json)


def main():
    app = QApplication(sys.argv)
    ex = YACMT()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
