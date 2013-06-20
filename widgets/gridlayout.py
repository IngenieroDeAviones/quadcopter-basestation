#! /usr/bin/env python3


from PyQt4 import QtGui,  QtCore


class GridLayout(QtGui.QLayout):
    def __init__(self, grid=[8, 5], parent=None):
        super().__init__(parent)
        try:
            grid[1]
            self.grid= grid
        except TypeError:
            self.grid= [grid, grid]

        self.rows = []


    def addItem(self, item, column=None, row=None):
        if column is None or row is None:
            self.rows.append([item])
        else:
            while len(self.rows) <= row:
                self.rows.append([])
            while len(self.rows[row]) <= column:
                self.rows[row].append(None)
            self.rows[row][column] = item


    def addWidget(self, widget, column=None, row=None):
        item = QtGui.QWidgetItem(widget)
        self.addItem(item, column, row)


    def count(self):
        return sum(map(len, self.items()))


    def sizeHint(self):
        return QtCore.QSize(self.grid[0] * 32, self.grid[1] * 32)


    def itemAt(self, index):
        try:
            return self.items()[index]
        except IndexError:
            return None


    def takeAt(self, index):
        i = 0
        for j,row in enumerate(self.rows):
            row = filter(bool, row)
            if len(row) < index - i:
                item = row[index - i]
                self.rows[j].remove(item)
                return item
            i += len(row)
        return None


    def setGeometry(self, rect):
        self.doLayout(rect)


    def items(self):
        a = []
        map(a.extend, self.rows)
        return tuple(filter(bool, a))


    def doLayout(self, rect):
        gridSize = min(rect.width() / self.grid[0], rect.height() / self.grid[1])
        for i, row in enumerate(self.rows):
            for j, item in enumerate(row):
                if item:
                    item.setGeometry(QtCore.QRect(j * gridSize, i * gridSize,
                                                  item.widget().colSpan * gridSize, item.widget().rowSpan * gridSize))
