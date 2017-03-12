import numpy as np
import style

from PyQt5 import QtWidgets, QtGui, QtCore


class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.resize(700, 700)
        self.setFixedSize(self.size())
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-1.5*size.width())/2,
                  (screen.height()-size.height())/2)
        self.row = 12
        self.col = 12

        self.field = GameField(self.row, self.col)
        self.cells = [[None for x in range(self.col)] for y in range(self.row)]
        grid = QtWidgets.QGridLayout()
        for x in range(self.row):
            for y in range(self.col):
                self.cells[x][y] = QtWidgets.QLabel()
                grid.addWidget(self.cells[x][y], x, y)
        self.setLayout(grid)

        self.drawField()

    def drawField(self):
        for x in range(self.row):
            for y in range(self.col):
                try:
                    self.cells[x][y].setStyleSheet(
                        style.colors[self.field.get(x, y)])
                    if self.field.get(x, y) != 0:
                        self.cells[x][y].setText(str(self.field.get(x, y)))
                    else:
                        self.cells[x][y].setText('')
                except KeyError:
                    self.message('Win', "Score:  "+str(self.field.get(x, y)))
                    self.close()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
        elif event.key() == QtCore.Qt.Key_Up:
            self.moveField('up')
        elif event.key() == QtCore.Qt.Key_Down:
            self.moveField('down')
        elif event.key() == QtCore.Qt.Key_Right:
            self.moveField('right')
        elif event.key() == QtCore.Qt.Key_Left:
            self.moveField('left')

    def moveField(self, direction):
        if direction in ['up', 'down']:
            for y in range(self.col):
                col = self.field.getColumn(y)
                if direction == 'up':
                    for x in range(len(col)-1):
                        if col[x] == col[x+1]:
                            col[x] *= 2
                            col[x+1] = 0
                else:
                    for x in range(1, len(col)):
                        if col[len(col)-x] == col[len(col)-1-x]:
                            col[len(col)-x] *= 2
                            col[len(col)-1-x] = 0
                self.field.setColumn(y, col[col.nonzero()], direction)

        elif direction in ['right', 'left']:
            for y in range(self.row):
                row = self.field.getRow(y)
                if direction == 'left':
                    for x in range(len(row)-1):
                        if row[x] == row[x+1]:
                            row[x] *= 2
                            row[x+1] = 0
                else:
                    for x in range(1, len(row)):
                        if row[len(row)-x] == row[len(row)-1-x]:
                            row[len(row)-x] *= 2
                            row[len(row)-1-x] = 0
                self.field.setRow(y, row[row.nonzero()], direction)

        result = self.field.generateRandomCell()
        self.drawField()
        if not result:
            self.message('Loser!', 'You lose')

    def message(self, name, message):
        reply = QtWidgets.QMessageBox.question(self, name, message,
                                               QtWidgets.QMessageBox.Yes)
        return reply


class GameField():
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.theField = np.zeros((row, col), dtype='int64')
        self.generateRandomCell(2)
        self.generateRandomCell(2)

    def get(self, row, col):
        return self.theField[row][col]

    def set(self, row, col, state):
        self.theField[row][col] = state

    def getColumn(self, col):
        b = self.theField[:, col:col+1].flatten()
        return b[b.nonzero()]

    def setColumn(self, col, array, flag):
        if flag == 'up':
            for x in range(self.row):
                self.theField[x][col] = array[x] if len(array) > x else 0
        elif flag == 'down':
            for x in range(self.row):
                self.theField[x][col] = array[len(array)-self.row+x] \
                    if len(array) > self.col-1-x else 0

    def getRow(self, row):
        b = self.theField[row]
        return b[b.nonzero()]

    def setRow(self, row, array, flag):
        if flag == 'left':
            for x in range(self.col):
                self.theField[row][x] = array[x] if len(array) > x else 0
        elif flag == 'right':
            for x in range(self.col):
                self.theField[row][x] = array[len(array)-self.col+x] \
                        if len(array) > self.col-1-x else 0

    def generateRandomCell(self, num=0):
        idx = np.argwhere(self.theField == 0)
        np.random.shuffle(idx)
        cells = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 4, 8]
        np.random.shuffle(cells)
        if idx.shape[0] != 0:
            if num:
                self.theField[idx[0][0], idx[0][1]] = num
            else:
                self.theField[idx[0][0], idx[0][1]] = cells[0]
            return 1
        else:
            return 0


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    w = Widget()
    w.show()
    app.exec_()
