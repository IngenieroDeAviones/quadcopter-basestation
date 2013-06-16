#! /usr/bin/env python3


from PyQt4 import QtGui,  QtCore

class FloatPriority:
    LeftThenTop = 0
    TopThenLeft = 1


class FloatLayout(QtGui.QLayout):
    def __init__(self, grid=[8, 5], priority=FloatPriority.LeftThenTop, parent=None):
        super().__init__(parent)
        self.priority = priority
        try:
            grid[1]
            self.grid= grid
        except TypeError:
            self.grid= [grid, grid]

        self.items = []


    def addItem(self, item, column=None, row=None):
        if column is None or row is None:
            self.items.append([item])
        else:
            while len(self.items) <= row:
                self.items.append([])
            self.items[row].insert(column, item)


    def addWidget(self, widget, column=None, row=None):
        item = QtGui.QWidgetItem(widget)
        self.addItem(item, column, row)


    def count(self):
        return sum(map(len, self.items))



    def itemAt(self, index):
        i = 0
        for row in self.items:
            if len(row) < index - i:
                return row[index - i]
            i += len(row)
        return None


    def takeAt(self, index):
        i = 0
        for row in self.items:
            if len(row) < index - i:
                item = row[index - i]
                del row[index - i]
                return item
            i += len(row)
        return None


    def setGeometry(self, rect):
        self.doLayout(rect)


    def sizeHint(self):
        gridSize = min(self.geometry().width() / self.grid[0], self.geometry().height() / self.grid[1])
        return QtCore.QSize(gridSize * max(map(len, self.items)),
                            gridSize * len(self.items))


    def doLayout(self, rect):
        gridSize = min(rect.width() / self.grid[0], rect.height() / self.grid[1])
        rowLengths = [0] * len(self.items)
        for row, line in enumerate(self.items):
            for item in line:
                if item.widget().isVisible():
                    rowSpan = item.widget().rowSpan
                    colSpan = item.widget().colSpan
                    x = max(rowLengths[row:max(row + rowSpan, len(rowLengths))])
                    item.setGeometry(QtCore.QRect(x, gridSize * row, gridSize * colSpan, gridSize * rowSpan))
                    for i in range(rowSpan):
                        try:
                            rowLengths[row + i] = x + colSpan * gridSize
                        except:
                            pass
