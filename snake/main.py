import style
import numpy as np
from PyQt5 import QtWidgets, QtGui, QtCore


class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.resize(700, 700)
        self.setFixedSize(self.size())
        self.setWindowTitle('Snake')
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-1.5*size.width())/2,
                  (screen.height()-2*size.height())/2)

        self.row, self.col = 20, 20
        self.score = 0
        self.direction = 'right'
        self.snake = [[2, 2], [1, 2], [1, 1]]
        self.field = GameField(self.row, self.col)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update_field)
        for x in self.snake:
            self.field.set(x, 1)
        self.cells = [[None for x in range(self.col)] for y in range(self.row)]
        grid = QtWidgets.QGridLayout()
        for x in range(self.row):
            for y in range(self.col):
                self.cells[x][y] = QtWidgets.QLabel()
                grid.addWidget(self.cells[x][y], x, y)
        self.setLayout(grid)

        self.food = self.field.generateRandomCell()
        self.initField()
        self.timer.start(100)

    def initField(self):
        for x in range(self.row):
            for y in range(self.col):
                self.drawObject([x, y], 'back')
        self.drawObject(self.snake[0], 'snake')
        self.drawObject(self.food, 'food')

    def drawObject(self, obj, type):
        self.cells[obj[0]][obj[1]].setStyleSheet(style.colors[type])

    def _update_field(self):
        head, tail = self.snake[0].copy(), self.snake.pop()
        if self.direction == 'right' and head[1] < self.col-1:
            head[1] += 1
        elif self.direction == 'left' and head[1] > 0:
            head[1] -= 1
        elif self.direction == 'down' and head[0] < self.row-1:
            head[0] += 1
        elif self.direction == 'up' and head[0] > 0:
            head[0] -= 1
        self.snake.insert(0, head)
        self.field.set(head, 1)
        self.field.set(tail, 0)
        if head == self.food:
            self.score += 1
            self.food = self.field.generateRandomCell()
            if (100 - self.score*5) > 50:
                self.timer.stop()
                self.timer.start(100-self.score*5)   # a bit more faster
            self.drawObject(self.food, 'food')
        self.drawObject(tail, 'back')
        self.drawObject(self.snake[0], 'snake')

    def message(self, name, message):
        reply = QtWidgets.QMessageBox.question(self, name, message,
                                               QtWidgets.QMessageBox.Yes)
        return reply

    def closeEvent(self, event):
        self.timer.stop()
        self.message("Score", str(self.score))
        event.accept()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
        elif event.key() == QtCore.Qt.Key_Up:
            self.direction = 'up'
        elif event.key() == QtCore.Qt.Key_Down:
            self.direction = 'down'
        elif event.key() == QtCore.Qt.Key_Right:
            self.direction = 'right'
        elif event.key() == QtCore.Qt.Key_Left:
            self.direction = 'left'


class GameField():
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.theField = np.zeros((row, col), dtype='int64')

    def get(self, cell):
        return self.theField[cell[0]][cell[1]]

    def set(self, cell, state):
        self.theField[cell[0]][cell[1]] = state

    def generateRandomCell(self):
        idx = np.argwhere(self.theField == 0)
        np.random.shuffle(idx)
        self.theField[idx[0][0], idx[0][1]] = 2
        return [idx[0][0], idx[0][1]]

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    w = Widget()
    w.show()
    app.exec_()
