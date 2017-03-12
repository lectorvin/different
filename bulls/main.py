from PyQt5 import QtWidgets, QtCore, QtGui
from functools import partial
import random

icons = {
    'plus': 'icons/plus.png',
    'minus': 'icons/minus.png',
    'cow': 'icons/cow.png',
    'bull': 'icons/bull.png'
}

button = """
    QPushButton {
        border-radius: 10px;
        width: 20px;
        height: 20px;
    }
"""

main = """
    QLabel {
        font-size: 15px;
        qproperty-alignment: AlignCenter;
    }
"""

class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.resize(240, 180)
        self.setFixedSize(self.size())
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-2*size.width())/2,
                  (screen.height()-3*size.height())/2)
        self.number = []
        self.n = [0, 0, 0, 0]
        self.turn = 20
        self.labels = [None, None, None, None]
        plus = [None, None, None, None]
        minus = [None, None, None, None]

        for x in range(4):
            self.labels[x] = QtWidgets.QLabel(str(self.n[x]))
            minus[x] = Button(self.minus, x, 'minus')
            plus[x] = Button(self.add, x, 'plus')

        bull_face = QtWidgets.QLabel()
        bull_face.setPixmap(QtGui.QPixmap(icons['bull']).
                            scaled(QtCore.QSize(32, 32),
                                   QtCore.Qt.KeepAspectRatio))
        self.bull_n = 0
        self.bull_label = QtWidgets.QLabel(str(self.bull_n))
        cow_face = QtWidgets.QLabel()
        cow_face.setPixmap(QtGui.QPixmap(icons['cow']).
                           scaled(QtCore.QSize(32, 32),
                                  QtCore.Qt.KeepAspectRatio))
        self.cow_n = 0
        self.cow_label = QtWidgets.QLabel(str(self.cow_n))

        turn = QtWidgets.QLabel('turn')
        self.turn_count = QtWidgets.QLabel(str(self.turn))
        check_button = Button(self.check, name='check', style=None)
        start = Button(self.start, name='Start', style=None)
        
        w = QtWidgets.QWidget()
        grid = QtWidgets.QGridLayout()
        grid.addWidget(bull_face, 1, 1, 2, 2)
        grid.addWidget(cow_face, 3, 1, 2, 2)
        grid.addWidget(self.bull_label, 2, 3)
        grid.addWidget(self.cow_label, 4, 3)
        for x in range(4):
            grid.addWidget(plus[x], 2, 5+x)
            grid.addWidget(self.labels[x], 3, 5+x)
            grid.addWidget(minus[x], 4, 5+x)
        grid.addWidget(check_button, 5, 5, 3, 3)
        grid.addWidget(turn, 3, 9)
        grid.addWidget(self.turn_count, 4, 9)
        w.setLayout(grid)
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(w)
        vbox.addWidget(check_button)
        vbox.addWidget(start)

        self.setLayout(vbox)
        self.setStyleSheet(main)

    def add(self, num):
        self.n[num] = 0 if self.n[num] == 9 else self.n[num]+1
        self.labels[num].setText(str(self.n[num]))

    def minus(self, num):
        self.n[num] = 9 if self.n[num] == 0 else self.n[num]-1
        self.labels[num].setText(str(self.n[num]))

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()

    def start(self):
        temp = [x for x in range(10)]
        random.shuffle(temp)
        self.number = temp[:4]
        self.turn = 20
        self.turn_count.setText(str(self.turn))
        print(self.number)

    def check(self):
        if not self.number:
            self.message('Error', 'You should start')
            return
        if len(set(self.n)) == 4:
            bull = sum([1 for x in range(4) if self.n[x] == self.number[x]])
            cow = sum([1 for x in range(4) if self.n[x] in self.number]) - bull
            self.bull_label.setText(str(bull))
            self.cow_label.setText(str(cow))
            self.turn -= 1
            self.turn_count.setText(str(self.turn))
            if bull == 4:
                self.message('Winner', 'You won!')
                self.number = []
            elif self.turn == 0:
                self.message('Loser', 'You lose!')
                self.number = []
        else:
            self.message('Error', 'All numbers should be different')

    def message(self, name, message):
        reply = QtWidgets.QMessageBox.question(self, name, message,
                                               QtWidgets.QMessageBox.Yes)
        return reply



class Button(QtWidgets.QPushButton):
    def __init__(self, action=None, num=None, icon='', name='', 
                 style=button, parent=None):
        QtWidgets.QPushButton.__init__(self, parent)
        self.setText(name)
        if icon in icons.keys():
            self.setIcon(QtGui.QIcon(icons[icon]))
            self.setIconSize(QtCore.QSize(20, 20))
        if action is not None:
            if num is not None:
                self.clicked.connect(partial(action, num))
            else:
                self.clicked.connect(action)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setStyleSheet(style)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    w = Widget()
    w.show()
    app.exec_()
