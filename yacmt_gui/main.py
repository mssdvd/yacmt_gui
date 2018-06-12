import datetime
import json
import sys

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QAction, QApplication, QGridLayout, QLabel,
                             QLCDNumber, QMainWindow, QPushButton, QTabWidget,
                             QWidget, qApp)
from sqlalchemy.exc import OperationalError

from .db import init_db, insert_report, upload_reports


class YacmtGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        init_db()
        self.initUI()

    def initUI(self):
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.monitor_tab = Monitor(self)
        self.tabs.addTab(self.monitor_tab, "Monitor")
        self.settings_tab = Settings(self)
        self.tabs.addTab(self.settings_tab, "Settings")

        exit_action = QAction(
            QIcon.fromTheme("application-exit"), "Exit", self)
        exit_action.triggered.connect(qApp.quit)

        upload_action = QAction("Upload", self)
        upload_action.triggered.connect(self._upload_reports)

        self.toolbar = self.addToolBar("Actions")
        self.toolbar.addAction(exit_action)
        self.toolbar.addAction(upload_action)

        self.setGeometry(0, 0, 320, 240)
        self.setWindowTitle('YACMT')
        self.show()

    def _upload_reports(self):
        try:
            upload_reports()
        except OperationalError as e:
            from PyQt5.QtWidgets import QErrorMessage
            error_dialog = QErrorMessage()
            error_dialog.showMessage(str(e))


class Monitor(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        # Grid Layout
        grid = QGridLayout(self)

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

        # Engine load
        self.lcdLoad = QLCDNumber()
        grid.addWidget(self.lcdLoad, 0, 2)
        labelLoad = QLabel(self.lcdLoad)
        labelLoad.setText("Engine load")

        # Engine cool temperature
        self.lcdCoolTemp = QLCDNumber()
        grid.addWidget(self.lcdCoolTemp, 1, 0)
        labelCoolTemp = QLabel(self.lcdCoolTemp)
        labelCoolTemp.setText("Coolant temp")

        # Control Module voltage
        self.lcdCMV = QLCDNumber()
        grid.addWidget(self.lcdCMV, 1, 1)
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
        self.report_timer.start(10000)

        self.setGeometry(0, 0, 320, 240)
        self.setWindowTitle('YACMT')
        self.show()

    def _update_display(self):
        try:
            yacmt_json = json.loads(open("/tmp/yacmt-server.json").read())
        except:
            return
        for k, v in yacmt_json.items():
            if v in ("NO DATA", "ERROR", "?"):
                yacmt_json[k] = 0
        self.lcdRPM.display(yacmt_json.get("eng_rpm"))
        self.lcdSpeed.display(yacmt_json.get("speed"))
        self.lcdLoad.display(yacmt_json.get("eng_load"))
        self.lcdCoolTemp.display(yacmt_json.get("eng_cool_temp"))
        self.lcdCMV.display(yacmt_json.get("control_mod_voltage"))
        try:
            self.lcdRunTime.display(
                str(datetime.timedelta(seconds=yacmt_json.get("run_time"))))
        except TypeError:
            self.lcdRunTime.display("00:00:00")

    def _new_report(self):
        try:
            yacmt_json = json.loads(open("/tmp/yacmt-server.json").read())
            insert_report(yacmt_json)
        except:
            return


class Settings(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.delete_button = QPushButton("Delete", self)
        self.delete_button.setToolTip("Delete the local database")
        self.delete_button.clicked.connect(self._delete_db)
        self.delete_button.move(300, 20)
        self.delete_label = QLabel(self)
        self.delete_label.setText("Delete the local database")
        self.delete_label.move(10, 25)

    def _delete_db(self):
        import os
        try:
            os.remove(os.path.expanduser("~") + "/yacmt.db")
        except:
            pass


def main():
    app = QApplication(sys.argv)
    yacmt_gui = YacmtGUI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
