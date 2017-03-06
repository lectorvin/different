import sys
import pyscreenshot as ImageGrab
import cv2 as cv
import numpy as np
from PyQt4 import QtGui


class Window(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.createTrayIcon()
        self.ok = QtGui.QPushButton("&Ok")
        self.ok.clicked.connect(self.close)
        layout = QtGui.QGridLayout()
        layout.addWidget(self.ok)
        self.setLayout(layout)

    def createTrayIcon(self):
        trayIconMenu = QtGui.QMenu(self)
        trayIconMenu.addAction(QtGui.QAction("Grabber", self,
                               triggered=self.grabber))
        trayIconMenu.addAction(QtGui.QAction("Quit", self,
                               triggered=sys.exit))

        self.trayIcon = QtGui.QSystemTrayIcon(
                QtGui.QIcon("grab.png"), self)
        self.trayIcon.setContextMenu(trayIconMenu)

    def closeEvent(self, event):
        self.trayIcon.show()
        self.trayIcon.showMessage("Grabber", "Now grab from tray")
        event.accept()

    def grabber(self):
        im = ImageGrab.grab()
        im.save("screenshot.png")
        cv.imshow("IMage", np.array(im)[:, :, ::-1])
        cv.waitKey(500)
        sys.exit()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    QtGui.QApplication.setQuitOnLastWindowClosed(False)
    w = Window()
    w.show()
    sys.exit(app.exec_())
