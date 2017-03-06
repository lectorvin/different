import sys
from PyQt4 import QtGui, QtCore


class Window(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.resize(200, 100)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update_time)
        self.time_label = QtGui.QLabel()
        self.hour = QtGui.QSpinBox()
        self.hour.setRange(0, 23)
        self.minute = QtGui.QSpinBox()
        self.minute.setRange(0, 59)
        self.seconds = QtGui.QSpinBox()
        self.seconds.setRange(0, 59)
        self.start_button = QtGui.QPushButton("Start")
        self.start_button.clicked.connect(self._start)
        self.stop_button = QtGui.QPushButton("Stop")
        self.stop_button.clicked.connect(self._stop)
        self.exit = QtGui.QPushButton("E&xit")
        self.exit.clicked.connect(self.close)

        layout = QtGui.QGridLayout()
        layout.addWidget(self.time_label, 1, 2)
        layout.addWidget(self.hour, 2, 1)
        layout.addWidget(self.minute, 2, 2)
        layout.addWidget(self.seconds, 2, 3)
        layout.addWidget(self.start_button, 3, 2)
        layout.addWidget(self.stop_button, 3, 3)
        layout.addWidget(self.exit, 4, 2)
        self.setLayout(layout)
        self.time_label.setText(QtCore.QTime(0, 0, 0).
                                toString(QtCore.Qt.ISODate))

    def _start(self):
        if (self.hour.value()+self.minute.value()+self.seconds.value() == 0):
            return
        self.countdown = QtCore.QTime(self.hour.value(),
                                      self.minute.value(),
                                      self.seconds.value())
        self.time_label.setText(self.countdown.toString(QtCore.Qt.ISODate))
        self.timer.start(1000)

    def _stop(self):
        self.timer.stop()
        self.time_label.setText(QtCore.QTime(0, 0, 0).
                                toString(QtCore.Qt.ISODate))

    def _update_time(self):
        self.countdown = self.countdown.addSecs(-1)
        if self.countdown <= QtCore.QTime(0, 0, 0):
            self.timer.stop()
            QtGui.QMessageBox.question(self, 'End', "Time",
                                       QtGui.QMessageBox.Yes)
        self.time_label.setText(self.countdown.toString(QtCore.Qt.ISODate))


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    widget = Window()
    widget.show()
    app.exec_()
