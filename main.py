import datetime
import sys

import requests
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import (QApplication, QGridLayout, QLabel, QLCDNumber,
                             QWidget)

from db import init_db, insert_report


class YacmtGUI(QWidget):
    def __init__(self):
        super().__init__()
        init_db()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()

        # Speed
        self.lcdSpeed = QLCDNumber()
        grid.addWidget(self.lcdSpeed, 0, 0)
        labelSpeed = QLabel(self.lcdSpeed)
        labelSpeed.setText("Speed")

        # RPM
        self.lcdRPM = QLCDNumber()
        grid.addWidget(self.lcdRPM, 0, 1)
        labelRPM = QLabel(self.lcdRPM)
        labelRPM.setText("RPM")

        # Control Module voltage
        self.lcdCMV = QLCDNumber()
        grid.addWidget(self.lcdCMV, 1, 0)
        labelCMV = QLabel(self.lcdCMV)
        labelCMV.setText("CMV")

        # Run time
        self.lcdRunTime = QLCDNumber()
        self.lcdRunTime.setDigitCount(8)
        grid.addWidget(self.lcdRunTime)
        labelRunTime = QLabel(self.lcdRunTime)
        labelRunTime.setText("Run Time")

        # Set timers
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
        yacmt_json = requests.get("http://localhost:8080").json()
        self.lcdRPM.display(yacmt_json.get("eng_rpm"))
        self.lcdSpeed.display(yacmt_json.get("speed"))
        self.lcdCMV.display(yacmt_json.get("control_mod_voltage"))
        self.lcdRunTime.display(
            str(datetime.timedelta(seconds=yacmt_json.get("run_time"))))

    def _new_report(self):
        yacm_json = requests.get("http://localhost:8080").json()
        insert_report(yacm_json)


def main():
    app = QApplication(sys.argv)
    yacmt_gui = YacmtGUI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
