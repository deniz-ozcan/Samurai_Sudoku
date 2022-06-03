from sudoku import Ui_sudoku
from sys import exit, argv
from time import sleep
from csv import reader
from os.path import dirname, join
import numpy as np

current_dir = dirname(__file__)
file_path = join(current_dir, "./sudokus.csv")
from PyQt5.QtGui import (
QColor,
)
from PyQt5.QtCore import (
    Qt,
    QThread,
    pyqtSignal,
)
from PyQt5.QtWidgets import (
    QAbstractSlider,
    QTableWidgetItem,
    QApplication,
    QMainWindow,
    QMessageBox,
    QGraphicsOpacityEffect as glory,
    QLCDNumber,
    QListWidgetItem,
)


class TimerClass(QThread):

    any_signal = pyqtSignal(int)

    def __init__(self, parent=None, seconds=0):
        super(TimerClass, self).__init__(parent)
        self.is_running = True
        self.seconds = seconds

    def run(self):
        t = self.seconds
        while True:
            t -= 1
            sleep(1)
            self.any_signal.emit(t)

    def stop(self):
        self.is_running = False
        self.terminate()


class SolverClass(QThread):
    any_signal = pyqtSignal(str, str, str)

    def __init__(self, parent=None, table=[], name=None):
        super(SolverClass, self).__init__(parent)
        self.is_running = True
        self.table = table
        self.name = name

    def run(self):
        tablerows = np.array(self.table).reshape(9, 9)
        firstStr = ""
        for _ in range(0, 9):
            firstStr += str(tablerows[_])
        secondStr = ""
        for i in firstStr:
            if i == "[":
                pass
            elif i == "]":
                pass
            elif i == " ":
                pass
            else:
                secondStr += i

        def crover(A, B):
            return [a + b for a in A for b in B]

        digits = "123456789"
        rows = "ABCDEFGHI"
        cols = digits
        squares = crover(rows, cols)
        unitlist = (
            [crover(rows, c) for c in cols]
            + [crover(r, cols) for r in rows]
            + [
                crover(rs, cs)
                for rs in ("ABC", "DEF", "GHI")
                for cs in ("123", "456", "789")
            ]
        )
        units = dict((s, [u for u in unitlist if s in u]) for s in squares)
        peers = dict((s, set(sum(units[s], [])) - set([s])) for s in squares)

        def gridParsing(grid):
            values = dict((s, digits) for s in squares)
            for s, d in list(valuesofGrid(grid).items()):
                if d in digits and not assingnment(values, s, d):
                    return False
            return values

        def valuesofGrid(grid):
            chars = [c for c in grid if c in digits or c in "0."]
            assert len(chars) == 81
            return dict(list(zip(squares, chars)))

        def assingnment(values, s, d):
            other_values = values[s].replace(d, "")
            if all(unnecessaryElements(values, s, d2) for d2 in other_values):
                return values
            else:
                return False

        def unnecessaryElements(values, s, d):
            if d not in values[s]:
                return values
            values[s] = values[s].replace(d, "")
            if len(values[s]) == 0:
                return False
            elif len(values[s]) == 1:
                d2 = values[s]
                if not all(unnecessaryElements(values, s2, d2) for s2 in peers[s]):
                    return False
            for u in units[s]:
                dplaces = [s for s in u if d in values[s]]
                if len(dplaces) == 0:
                    return False
                elif len(dplaces) == 1:
                    if not assingnment(values, dplaces[0], d):
                        return False
            return values

        def signalSender(valuesx):
            for r in rows:
                self.any_signal.emit(
                    "".join(valuesx[r + c] for c in cols), r, self.name
                )

        def solve(grid):
            return valuesSearching(gridParsing(grid))

        def valuesSearching(values):
            if values is False:
                return False
            if all(len(values[s]) == 1 for s in squares):
                return signalSender(values)
            n, s = min((len(values[s]), s) for s in squares if len(values[s]) > 1)
            return some(
                valuesSearching(assingnment(values.copy(), s, d)) for d in values[s]
            )

        def some(seq):
            for e in seq:
                if e == True:
                    return e
            return False

        solve(secondStr)

    def stop(self):
        self.is_running = False
        self.terminate()


class Sudoku(QMainWindow, Ui_sudoku):
    countdown = 3600
    t1, t2, t3, t4, t5 = 0, 0, 0, 0, 0

    def __init__(self):
        super(Sudoku, self).__init__()
        self.setupUi(self)
        self.timer.setDigitCount(8)
        self.timer.setSegmentStyle(QLCDNumber.Flat)
        x = 3600
        mins, secs = divmod(x, 60)
        hours, mins = divmod(mins, 60)
        timer = "{:02d}:{:02d}:{:02d}".format(hours, mins, secs)
        self.timer.display(timer)
        self.timerframe.setGraphicsEffect(glory(opacity=0.0))
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.timepush.clicked.connect(self.settimerslider)
        self.minimize.clicked.connect(self.showMinimized)
        self.closeBut.clicked.connect(self.close)
        self.getNameOfSudoku()
        self.LoadButton.clicked.connect(self.getsudoku)
        self.solveButton.clicked.connect(self.itemsofTable)
        self.restartButton.clicked.connect(self.clearing)
        self.thread = {}
        for a in range(0, 21):
            for b in range(0, 21):
                self.Asudokutable.setColumnWidth(b, 23)
                self.Asudokutable.setRowHeight(a, 23)

        def moveWindow(event):
            if self.isMaximized() == False:
                if event.buttons() == Qt.LeftButton:
                    self.move(self.pos() + event.globalPos() - self.clickPosition)
                    self.clickPosition = event.globalPos()
                    event.accept()

        self.headerFrame.mouseMoveEvent = moveWindow

    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()

    def start_worker_1(self):
        self.thread[6] = TimerClass(parent=None, seconds=Sudoku.countdown)
        self.thread[6].start()
        self.thread[6].any_signal.connect(self.lcd_number)

    def stop_worker_1(self):
        self.thread[6].stop()

    def itemsofTable(self):
        pro = 0
        for j in range(0, 21):
            if self.Asudokutable.item(0, j) == None:
                pro += 1
        if pro >= 21:
            QMessageBox.about(
                self,
                "Warning",
                '<p><span style="font-size:15pt; color:white; font-weight:600;">Table has no element to solve.</span></p>',
            )
        else:
            topLeft = []
            topRight = []
            middle = []
            bottomLeft = []
            bottomRight = []
            rangeoftable = [
                ((0, 9), (0, 9)),
                ((0, 9), (12, 21)),
                ((6, 15), (6, 15)),
                ((12, 21), (0, 9)),
                ((12, 21), (12, 21)),
            ]
            count = 0
            for i in rangeoftable:
                for a in range(i[0][0], i[0][1]):
                    for b in range(i[1][0], i[1][1]):
                        if count == 0:
                            if self.Asudokutable.item(a, b) != None:
                                topLeft.append(int(self.Asudokutable.item(a, b).text()))
                            else:
                                topLeft.append(0)
                        if count == 1:
                            if self.Asudokutable.item(a, b) != None:
                                topRight.append(
                                    int(self.Asudokutable.item(a, b).text())
                                )
                            else:
                                topRight.append(0)
                        if count == 2:
                            if self.Asudokutable.item(a, b) != None:
                                middle.append(int(self.Asudokutable.item(a, b).text()))
                            else:
                                middle.append(0)
                        if count == 3:
                            if self.Asudokutable.item(a, b) != None:
                                bottomLeft.append(
                                    int(self.Asudokutable.item(a, b).text())
                                )
                            else:
                                bottomLeft.append(0)
                        if count == 4:
                            if self.Asudokutable.item(a, b) != None:
                                bottomRight.append(
                                    int(self.Asudokutable.item(a, b).text())
                                )
                            else:
                                bottomRight.append(0)
                count += 1
            self.thread[0] = SolverClass(parent=None, table=topLeft, name="topLeft")
            self.thread[0].any_signal.connect(self.shower)
            self.thread[1] = SolverClass(parent=None, table=topRight, name="topRight")
            self.thread[1].any_signal.connect(self.shower)
            self.thread[2] = SolverClass(
                parent=None, table=bottomLeft, name="bottomLeft"
            )
            self.thread[2].any_signal.connect(self.shower)
            self.thread[3] = SolverClass(
                parent=None, table=bottomRight, name="bottomRight"
            )
            self.thread[3].any_signal.connect(self.shower)
            self.thread[4] = SolverClass(parent=None, table=middle, name="middle")
            self.thread[4].any_signal.connect(self.shower)

            self.thread[0].start()
            self.thread[1].start()
            self.thread[2].start()
            self.thread[3].start()
            self.thread[4].start()

    def shower(self, columns, rows, name):

        for qxr in range(0, 9):

            if name == "topLeft":

                if rows == "A":
                    item = QTableWidgetItem(str(columns[qxr]))
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    item.setForeground(QColor(0, 0, 255))
                    if self.Asudokutable.item(0, qxr) == None:
                        self.Asudokutable.setItem(0, qxr, item)
                        stringObject = (
                            "Step: Put "
                            + str(columns[qxr])
                            + " in TL at r"
                            + str(1)
                            + "c"
                            + str(qxr + 1)
                        )
                        item2 = QListWidgetItem(stringObject)
                        item2.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                        item2.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        item2.setForeground(QColor(255, 255, 255))
                        self.listWidget.addItem(item2)
                    else:
                        pass
                if rows == "B":
                    item = QTableWidgetItem(str(columns[qxr]))
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    item.setForeground(QColor(0, 0, 255))
                    if self.Asudokutable.item(1, qxr) == None:
                        self.Asudokutable.setItem(1, qxr, item)
                        stringObject = (
                            "Step: Put "
                            + str(columns[qxr])
                            + " in TL at r"
                            + str(2)
                            + "c"
                            + str(qxr + 1)
                        )
                        item2 = QListWidgetItem(stringObject)
                        item2.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                        item2.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        item2.setForeground(QColor(255, 255, 255))
                        self.listWidget.addItem(item2)
                    else:
                        pass
                if rows == "C":
                    item = QTableWidgetItem(str(columns[qxr]))
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    item.setForeground(QColor(0, 0, 255))
                    if self.Asudokutable.item(2, qxr) == None:
                        self.Asudokutable.setItem(2, qxr, item)
                        stringObject = (
                            "Step: Put "
                            + str(columns[qxr])
                            + " in TL at r"
                            + str(3)
                            + "c"
                            + str(qxr + 1)
                        )
                        item2 = QListWidgetItem(stringObject)
                        item2.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                        item2.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        item2.setForeground(QColor(255, 255, 255))
                        self.listWidget.addItem(item2)
                    else:
                        pass
                if rows == "D":
                    item = QTableWidgetItem(str(columns[qxr]))
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    item.setForeground(QColor(0, 0, 255))
                    if self.Asudokutable.item(3, qxr) == None:
                        self.Asudokutable.setItem(3, qxr, item)
                        stringObject = (
                            "Step: Put "
                            + str(columns[qxr])
                            + " in TL at r"
                            + str(4)
                            + "c"
                            + str(qxr + 1)
                        )
                        item2 = QListWidgetItem(stringObject)
                        item2.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                        item2.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        item2.setForeground(QColor(255, 255, 255))
                        self.listWidget.addItem(item2)
                    else:
                        pass
                if rows == "E":
                    item = QTableWidgetItem(str(columns[qxr]))
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    item.setForeground(QColor(0, 0, 255))
                    if self.Asudokutable.item(4, qxr) == None:
                        self.Asudokutable.setItem(4, qxr, item)
                        stringObject = (
                            "Step: Put "
                            + str(columns[qxr])
                            + " in TL at r"
                            + str(5)
                            + "c"
                            + str(qxr + 1)
                        )
                        item2 = QListWidgetItem(stringObject)
                        item2.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                        item2.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        item2.setForeground(QColor(255, 255, 255))
                        self.listWidget.addItem(item2)
                    else:
                        pass
                if rows == "F":
                    item = QTableWidgetItem(str(columns[qxr]))
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    item.setForeground(QColor(0, 0, 255))
                    if self.Asudokutable.item(5, qxr) == None:
                        self.Asudokutable.setItem(5, qxr, item)
                        stringObject = (
                            "Step: Put "
                            + str(columns[qxr])
                            + " in TL at r"
                            + str(6)
                            + "c"
                            + str(qxr + 1)
                        )
                        item2 = QListWidgetItem(stringObject)
                        item2.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                        item2.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        item2.setForeground(QColor(255, 255, 255))
                        self.listWidget.addItem(item2)
                    else:
                        pass
                if rows == "G":
                    item = QTableWidgetItem(str(columns[qxr]))
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    item.setForeground(QColor(0, 0, 255))
                    if self.Asudokutable.item(6, qxr) == None:
                        self.Asudokutable.setItem(6, qxr, item)
                        stringObject = (
                            "Step: Put "
                            + str(columns[qxr])
                            + " in TL at r"
                            + str(7)
                            + "c"
                            + str(qxr + 1)
                        )
                        item2 = QListWidgetItem(stringObject)
                        item2.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                        item2.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        item2.setForeground(QColor(255, 255, 255))
                        self.listWidget.addItem(item2)
                    else:
                        pass
                if rows == "H":
                    item = QTableWidgetItem(str(columns[qxr]))
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    item.setForeground(QColor(0, 0, 255))
                    if self.Asudokutable.item(7, qxr) == None:
                        self.Asudokutable.setItem(7, qxr, item)
                        stringObject = (
                            "Step: Put "
                            + str(columns[qxr])
                            + " in TL at r"
                            + str(8)
                            + "c"
                            + str(qxr + 1)
                        )
                        item2 = QListWidgetItem(stringObject)
                        item2.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                        item2.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        item2.setForeground(QColor(255, 255, 255))
                        self.listWidget.addItem(item2)
                    else:
                        pass
                if rows == "I":
                    item = QTableWidgetItem(str(columns[qxr]))
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    item.setForeground(QColor(0, 0, 255))
                    if self.Asudokutable.item(8, qxr) == None:
                        self.Asudokutable.setItem(8, qxr, item)
                        stringObject = (
                            "Step: Put "
                            + str(columns[qxr])
                            + " in TL at r"
                            + str(9)
                            + "c"
                            + str(qxr + 1)
                        )
                        item2 = QListWidgetItem(stringObject)
                        item2.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                        item2.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        item2.setForeground(QColor(255, 255, 255))
                        self.listWidget.addItem(item2)
                    else:
                        pass
                Sudoku.t1 += 1

            if name == "topRight":
                if rows == "A":
                    item = QTableWidgetItem(str(columns[qxr]))
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    item.setForeground(QColor(0, 0, 255))
                    if self.Asudokutable.item(0, qxr + 12) == None:
                        self.Asudokutable.setItem(0, qxr + 12, item)
                        stringObject = (
                            "Step: Put "
                            + str(columns[qxr])
                            + " in TR at r"
                            + str(1)
                            + "c"
                            + str(qxr + 1)
                        )
                        item2 = QListWidgetItem(stringObject)
                        item2.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                        item2.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        item2.setForeground(QColor(255, 255, 255))
                        self.listWidget.addItem(item2)
                    else:
                        pass
                if rows == "B":
                    item = QTableWidgetItem(str(columns[qxr]))
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    item.setForeground(QColor(0, 0, 255))
                    if self.Asudokutable.item(1, qxr + 12) == None:
                        self.Asudokutable.setItem(1, qxr + 12, item)
                        stringObject = (
                            "Step: Put "
                            + str(columns[qxr])
                            + " in TR at r"
                            + str(2)
                            + "c"
                            + str(qxr + 1)
                        )
                        item2 = QListWidgetItem(stringObject)
                        item2.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                        item2.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        item2.setForeground(QColor(255, 255, 255))
                        self.listWidget.addItem(item2)
                    else:
                        pass
                if rows == "C":
                    item = QTableWidgetItem(str(columns[qxr]))
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    item.setForeground(QColor(0, 0, 255))
                    if self.Asudokutable.item(2, qxr + 12) == None:
                        self.Asudokutable.setItem(2, qxr + 12, item)
                        stringObject = (
                            "Step: Put "
                            + str(columns[qxr])
                            + " in TR at r"
                            + str(3)
                            + "c"
                            + str(qxr + 1)
                        )
                        item2 = QListWidgetItem(stringObject)
                        item2.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                        item2.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        item2.setForeground(QColor(255, 255, 255))
                        self.listWidget.addItem(item2)
                    else:
                        pass
                if rows == "D":
                    item = QTableWidgetItem(str(columns[qxr]))
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    item.setForeground(QColor(0, 0, 255))
                    if self.Asudokutable.item(3, qxr + 12) == None:
                        self.Asudokutable.setItem(3, qxr + 12, item)
                        stringObject = (
                            "Step: Put "
                            + str(columns[qxr])
                            + " in TR at r"
                            + str(4)
                            + "c"
                            + str(qxr + 1)
                        )
                        item2 = QListWidgetItem(stringObject)
                        item2.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                        item2.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        item2.setForeground(QColor(255, 255, 255))
                        self.listWidget.addItem(item2)
                    else:
                        pass
                if rows == "E":
                    item = QTableWidgetItem(str(columns[qxr]))
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    item.setForeground(QColor(0, 0, 255))
                    if self.Asudokutable.item(4, qxr + 12) == None:
                        self.Asudokutable.setItem(4, qxr + 12, item)
                        stringObject = (
                            "Step: Put "
                            + str(columns[qxr])
                            + " in TR at r"
                            + str(5)
                            + "c"
                            + str(qxr + 1)
                        )
                        item2 = QListWidgetItem(stringObject)
                        item2.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                        item2.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        item2.setForeground(QColor(255, 255, 255))
                        self.listWidget.addItem(item2)
                    else:
                        pass
                if rows == "F":
                    item = QTableWidgetItem(str(columns[qxr]))
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    item.setForeground(QColor(0, 0, 255))
                    if self.Asudokutable.item(5, qxr + 12) == None:
                        self.Asudokutable.setItem(5, qxr + 12, item)
                        stringObject = (
                            "Step: Put "
                            + str(columns[qxr])
                            + " in TR at r"
                            + str(6)
                            + "c"
                            + str(qxr + 1)
                        )
                        item2 = QListWidgetItem(stringObject)
                        item2.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                        item2.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        item2.setForeground(QColor(255, 255, 255))
                        self.listWidget.addItem(item2)
                    else:
                        pass
                if rows == "G":
                    item = QTableWidgetItem(str(columns[qxr]))
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    item.setForeground(QColor(0, 0, 255))
                    if self.Asudokutable.item(6, qxr + 12) == None:
                        self.Asudokutable.setItem(6, qxr + 12, item)
                        stringObject = (
                            "Step: Put "
                            + str(columns[qxr])
                            + " in TR at r"
                            + str(7)
                            + "c"
                            + str(qxr + 1)
                        )
                        item2 = QListWidgetItem(stringObject)
                        item2.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                        item2.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        item2.setForeground(QColor(255, 255, 255))
                        self.listWidget.addItem(item2)
                    else:
                        pass
                if rows == "H":
                    item = QTableWidgetItem(str(columns[qxr]))
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    item.setForeground(QColor(0, 0, 255))
                    if self.Asudokutable.item(7, qxr + 12) == None:
                        self.Asudokutable.setItem(7, qxr + 12, item)
                        stringObject = (
                            "Step: Put "
                            + str(columns[qxr])
                            + " in TR at r"
                            + str(8)
                            + "c"
                            + str(qxr + 1)
                        )
                        item2 = QListWidgetItem(stringObject)
                        item2.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                        item2.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        item2.setForeground(QColor(255, 255, 255))
                        self.listWidget.addItem(item2)
                    else:
                        pass
                if rows == "I":
                    item = QTableWidgetItem(str(columns[qxr]))
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    item.setForeground(QColor(0, 0, 255))
                    if self.Asudokutable.item(8, qxr + 12) == None:
                        self.Asudokutable.setItem(8, qxr + 12, item)
                        stringObject = (
                            "Step: Put "
                            + str(columns[qxr])
                            + " in TR at r"
                            + str(9)
                            + "c"
                            + str(qxr + 1)
                        )
                        item2 = QListWidgetItem(stringObject)
                        item2.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                        item2.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        item2.setForeground(QColor(255, 255, 255))
                        self.listWidget.addItem(item2)
                    else:
                        pass
                Sudoku.t2 += 1

            if name == "middle":
                if rows == "A":
                    item = QTableWidgetItem(str(columns[qxr]))
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    item.setForeground(QColor(0, 0, 255))
                    if self.Asudokutable.item(0 + 6, qxr + 6) == None:
                        self.Asudokutable.setItem(0 + 6, qxr + 6, item)
                        stringObject = (
                            "Step: Put "
                            + str(columns[qxr])
                            + " in M at r"
                            + str(1)
                            + "c"
                            + str(qxr + 1)
                        )
                        item2 = QListWidgetItem(stringObject)
                        item2.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                        item2.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        item2.setForeground(QColor(255, 255, 255))
                        self.listWidget.addItem(item2)
                    else:
                        pass
                if rows == "B":
                    item = QTableWidgetItem(str(columns[qxr]))
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    item.setForeground(QColor(0, 0, 255))
                    if self.Asudokutable.item(1 + 6, qxr + 6) == None:
                        self.Asudokutable.setItem(1 + 6, qxr + 6, item)
                        stringObject = (
                            "Step: Put "
                            + str(columns[qxr])
                            + " in M at r"
                            + str(2)
                            + "c"
                            + str(qxr + 1)
                        )
                        item2 = QListWidgetItem(stringObject)
                        item2.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                        item2.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        item2.setForeground(QColor(255, 255, 255))
                        self.listWidget.addItem(item2)
                    else:
                        pass
                if rows == "C":
                    item = QTableWidgetItem(str(columns[qxr]))
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    item.setForeground(QColor(0, 0, 255))
                    if self.Asudokutable.item(2 + 6, qxr + 6) == None:
                        self.Asudokutable.setItem(2 + 6, qxr + 6, item)
                        stringObject = (
                            "Step: Put "
                            + str(columns[qxr])
                            + " in M at r"
                            + str(3)
                            + "c"
                            + str(qxr + 1)
                        )
                        item2 = QListWidgetItem(stringObject)
                        item2.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                        item2.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        item2.setForeground(QColor(255, 255, 255))
                        self.listWidget.addItem(item2)
                    else:
                        pass
                if rows == "D":
                    item = QTableWidgetItem(str(columns[qxr]))
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    item.setForeground(QColor(0, 0, 255))
                    if self.Asudokutable.item(3 + 6, qxr + 6) == None:
                        self.Asudokutable.setItem(3 + 6, qxr + 6, item)
                        stringObject = (
                            "Step: Put "
                            + str(columns[qxr])
                            + " in M at r"
                            + str(4)
                            + "c"
                            + str(qxr + 1)
                        )
                        item2 = QListWidgetItem(stringObject)
                        item2.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                        item2.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        item2.setForeground(QColor(255, 255, 255))
                        self.listWidget.addItem(item2)
                    else:
                        pass
                if rows == "E":
                    item = QTableWidgetItem(str(columns[qxr]))
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    item.setForeground(QColor(0, 0, 255))
                    if self.Asudokutable.item(4 + 6, qxr + 6) == None:
                        self.Asudokutable.setItem(4 + 6, qxr + 6, item)
                        stringObject = (
                            "Step: Put "
                            + str(columns[qxr])
                            + " in M at r"
                            + str(5)
                            + "c"
                            + str(qxr + 1)
                        )
                        item2 = QListWidgetItem(stringObject)
                        item2.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                        item2.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        item2.setForeground(QColor(255, 255, 255))
                        self.listWidget.addItem(item2)
                    else:
                        pass
                if rows == "F":
                    item = QTableWidgetItem(str(columns[qxr]))
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    item.setForeground(QColor(0, 0, 255))
                    if self.Asudokutable.item(5 + 6, qxr + 6) == None:
                        self.Asudokutable.setItem(5 + 6, qxr + 6, item)
                        stringObject = (
                            "Step: Put "
                            + str(columns[qxr])
                            + " in M at r"
                            + str(6)
                            + "c"
                            + str(qxr + 1)
                        )
                        item2 = QListWidgetItem(stringObject)
                        item2.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                        item2.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        item2.setForeground(QColor(255, 255, 255))
                        self.listWidget.addItem(item2)
                    else:
                        pass
                if rows == "G":
                    item = QTableWidgetItem(str(columns[qxr]))
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    item.setForeground(QColor(0, 0, 255))
                    if self.Asudokutable.item(6 + 6, qxr + 6) == None:
                        self.Asudokutable.setItem(6 + 6, qxr + 6, item)
                        stringObject = (
                            "Step: Put "
                            + str(columns[qxr])
                            + " in M at r"
                            + str(7)
                            + "c"
                            + str(qxr + 1)
                        )
                        item2 = QListWidgetItem(stringObject)
                        item2.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                        item2.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        item2.setForeground(QColor(255, 255, 255))
                        self.listWidget.addItem(item2)
                    else:
                        pass
                if rows == "H":
                    item = QTableWidgetItem(str(columns[qxr]))
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    item.setForeground(QColor(0, 0, 255))
                    if self.Asudokutable.item(7 + 6, qxr + 6) == None:
                        self.Asudokutable.setItem(7 + 6, qxr + 6, item)
                        stringObject = (
                            "Step: Put "
                            + str(columns[qxr])
                            + " in M at r"
                            + str(8)
                            + "c"
                            + str(qxr + 1)
                        )
                        item2 = QListWidgetItem(stringObject)
                        item2.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                        item2.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        item2.setForeground(QColor(255, 255, 255))
                        self.listWidget.addItem(item2)
                    else:
                        pass
                if rows == "I":
                    item = QTableWidgetItem(str(columns[qxr]))
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    item.setForeground(QColor(0, 0, 255))
                    if self.Asudokutable.item(8 + 6, qxr + 6) == None:
                        self.Asudokutable.setItem(8 + 6, qxr + 6, item)
                        stringObject = (
                            "Step: Put "
                            + str(columns[qxr])
                            + " in M at r"
                            + str(9)
                            + "c"
                            + str(qxr + 1)
                        )
                        item2 = QListWidgetItem(stringObject)
                        item2.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                        item2.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        item2.setForeground(QColor(255, 255, 255))
                        self.listWidget.addItem(item2)
                    else:
                        pass
                Sudoku.t3 += 1

            if name == "bottomLeft":
                if rows == "A":
                    item = QTableWidgetItem(str(columns[qxr]))
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    item.setForeground(QColor(0, 0, 255))
                    if self.Asudokutable.item(12, qxr) == None:
                        self.Asudokutable.setItem(12, qxr, item)
                        stringObject = (
                            "Step: Put "
                            + str(columns[qxr])
                            + " in BL at r"
                            + str(1)
                            + "c"
                            + str(qxr + 1)
                        )
                        item2 = QListWidgetItem(stringObject)
                        item2.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                        item2.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        item2.setForeground(QColor(255, 255, 255))
                        self.listWidget.addItem(item2)
                    else:
                        pass
                if rows == "B":
                    item = QTableWidgetItem(str(columns[qxr]))
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    item.setForeground(QColor(0, 0, 255))
                    if self.Asudokutable.item(13, qxr) == None:
                        self.Asudokutable.setItem(13, qxr, item)
                        stringObject = (
                            "Step: Put "
                            + str(columns[qxr])
                            + " in BL at r"
                            + str(2)
                            + "c"
                            + str(qxr + 1)
                        )
                        item2 = QListWidgetItem(stringObject)
                        item2.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                        item2.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        item2.setForeground(QColor(255, 255, 255))
                        self.listWidget.addItem(item2)
                    else:
                        pass
                if rows == "C":
                    item = QTableWidgetItem(str(columns[qxr]))
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    item.setForeground(QColor(0, 0, 255))
                    if self.Asudokutable.item(14, qxr) == None:
                        self.Asudokutable.setItem(14, qxr, item)
                        stringObject = (
                            "Step: Put "
                            + str(columns[qxr])
                            + " in BL at r"
                            + str(3)
                            + "c"
                            + str(qxr + 1)
                        )
                        item2 = QListWidgetItem(stringObject)
                        item2.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                        item2.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        item2.setForeground(QColor(255, 255, 255))
                        self.listWidget.addItem(item2)
                    else:
                        pass
                if rows == "D":
                    item = QTableWidgetItem(str(columns[qxr]))
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    item.setForeground(QColor(0, 0, 255))
                    if self.Asudokutable.item(15, qxr) == None:
                        self.Asudokutable.setItem(15, qxr, item)
                        stringObject = (
                            "Step: Put "
                            + str(columns[qxr])
                            + " in BL at r"
                            + str(4)
                            + "c"
                            + str(qxr + 1)
                        )
                        item2 = QListWidgetItem(stringObject)
                        item2.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                        item2.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        item2.setForeground(QColor(255, 255, 255))
                        self.listWidget.addItem(item2)
                    else:
                        pass
                if rows == "E":
                    item = QTableWidgetItem(str(columns[qxr]))
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    item.setForeground(QColor(0, 0, 255))
                    if self.Asudokutable.item(16, qxr) == None:
                        self.Asudokutable.setItem(16, qxr, item)
                        stringObject = (
                            "Step: Put "
                            + str(columns[qxr])
                            + " in BL at r"
                            + str(5)
                            + "c"
                            + str(qxr + 1)
                        )
                        item2 = QListWidgetItem(stringObject)
                        item2.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                        item2.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        item2.setForeground(QColor(255, 255, 255))
                        self.listWidget.addItem(item2)
                    else:
                        pass
                if rows == "F":
                    item = QTableWidgetItem(str(columns[qxr]))
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    item.setForeground(QColor(0, 0, 255))
                    if self.Asudokutable.item(17, qxr) == None:
                        self.Asudokutable.setItem(17, qxr, item)
                        stringObject = (
                            "Step: Put "
                            + str(columns[qxr])
                            + " in BL at r"
                            + str(6)
                            + "c"
                            + str(qxr + 1)
                        )
                        item2 = QListWidgetItem(stringObject)
                        item2.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                        item2.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        item2.setForeground(QColor(255, 255, 255))
                        self.listWidget.addItem(item2)
                    else:
                        pass
                if rows == "G":
                    item = QTableWidgetItem(str(columns[qxr]))
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    item.setForeground(QColor(0, 0, 255))
                    if self.Asudokutable.item(18, qxr) == None:
                        self.Asudokutable.setItem(18, qxr, item)
                        stringObject = (
                            "Step: Put "
                            + str(columns[qxr])
                            + " in BL at r"
                            + str(3)
                            + "c"
                            + str(qxr + 1)
                        )
                        item2 = QListWidgetItem(stringObject)
                        item2.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                        item2.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        item2.setForeground(QColor(255, 255, 255))
                        self.listWidget.addItem(item2)
                    else:
                        pass
                if rows == "H":
                    item = QTableWidgetItem(str(columns[qxr]))
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    item.setForeground(QColor(0, 0, 255))
                    if self.Asudokutable.item(19, qxr) == None:
                        self.Asudokutable.setItem(19, qxr, item)
                        stringObject = (
                            "Step: Put "
                            + str(columns[qxr])
                            + " in BL at r"
                            + str(8)
                            + "c"
                            + str(qxr + 1)
                        )
                        item2 = QListWidgetItem(stringObject)
                        item2.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                        item2.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        item2.setForeground(QColor(255, 255, 255))
                        self.listWidget.addItem(item2)
                    else:
                        pass
                if rows == "I":
                    item = QTableWidgetItem(str(columns[qxr]))
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    item.setForeground(QColor(0, 0, 255))
                    if self.Asudokutable.item(20, qxr) == None:
                        self.Asudokutable.setItem(20, qxr, item)
                        stringObject = (
                            "Step: Put "
                            + str(columns[qxr])
                            + " in BL at r"
                            + str(9)
                            + "c"
                            + str(qxr + 1)
                        )
                        item2 = QListWidgetItem(stringObject)
                        item2.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                        item2.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        item2.setForeground(QColor(255, 255, 255))
                        self.listWidget.addItem(item2)
                    else:
                        pass
                Sudoku.t4 += 1

            if name == "bottomRight":
                if rows == "A":
                    item = QTableWidgetItem(str(columns[qxr]))
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    item.setForeground(QColor(0, 0, 255))
                    if self.Asudokutable.item(12, qxr + 12) == None:
                        self.Asudokutable.setItem(12, qxr + 12, item)
                        stringObject = (
                            "Step: Put "
                            + str(columns[qxr])
                            + " in BR at r"
                            + str(1)
                            + "c"
                            + str(qxr + 1)
                        )
                        item2 = QListWidgetItem(stringObject)
                        item2.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                        item2.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        item2.setForeground(QColor(255, 255, 255))
                        self.listWidget.addItem(item2)
                    else:
                        pass
                if rows == "B":
                    item = QTableWidgetItem(str(columns[qxr]))
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    item.setForeground(QColor(0, 0, 255))
                    if self.Asudokutable.item(13, qxr + 12) == None:
                        self.Asudokutable.setItem(13, qxr + 12, item)
                        stringObject = (
                            "Step: Put "
                            + str(columns[qxr])
                            + " in BR at r"
                            + str(2)
                            + "c"
                            + str(qxr + 1)
                        )
                        item2 = QListWidgetItem(stringObject)
                        item2.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                        item2.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        item2.setForeground(QColor(255, 255, 255))
                        self.listWidget.addItem(item2)
                    else:
                        pass
                if rows == "C":
                    item = QTableWidgetItem(str(columns[qxr]))
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    item.setForeground(QColor(0, 0, 255))
                    if self.Asudokutable.item(14, qxr + 12) == None:
                        self.Asudokutable.setItem(14, qxr + 12, item)
                        stringObject = (
                            "Step: Put "
                            + str(columns[qxr])
                            + " in BR at r"
                            + str(3)
                            + "c"
                            + str(qxr + 1)
                        )
                        item2 = QListWidgetItem(stringObject)
                        item2.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                        item2.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        item2.setForeground(QColor(255, 255, 255))
                        self.listWidget.addItem(item2)
                    else:
                        pass
                if rows == "D":
                    item = QTableWidgetItem(str(columns[qxr]))
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    item.setForeground(QColor(0, 0, 255))
                    if self.Asudokutable.item(15, qxr + 12) == None:
                        self.Asudokutable.setItem(15, qxr + 12, item)
                        stringObject = (
                            "Step: Put "
                            + str(columns[qxr])
                            + " in BR at r"
                            + str(4)
                            + "c"
                            + str(qxr + 1)
                        )
                        item2 = QListWidgetItem(stringObject)
                        item2.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                        item2.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        item2.setForeground(QColor(255, 255, 255))
                        self.listWidget.addItem(item2)
                    else:
                        pass
                if rows == "E":
                    item = QTableWidgetItem(str(columns[qxr]))
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    item.setForeground(QColor(0, 0, 255))
                    if self.Asudokutable.item(16, qxr + 12) == None:
                        self.Asudokutable.setItem(16, qxr + 12, item)
                        stringObject = (
                            "Step: Put "
                            + str(columns[qxr])
                            + " in BR at r"
                            + str(5)
                            + "c"
                            + str(qxr + 1)
                        )
                        item2 = QListWidgetItem(stringObject)
                        item2.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                        item2.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        item2.setForeground(QColor(255, 255, 255))
                        self.listWidget.addItem(item2)
                    else:
                        pass
                if rows == "F":
                    item = QTableWidgetItem(str(columns[qxr]))
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    item.setForeground(QColor(0, 0, 255))
                    if self.Asudokutable.item(17, qxr + 12) == None:
                        self.Asudokutable.setItem(17, qxr + 12, item)
                        stringObject = (
                            "Step: Put "
                            + str(columns[qxr])
                            + " in BR at r"
                            + str(6)
                            + "c"
                            + str(qxr + 1)
                        )
                        item2 = QListWidgetItem(stringObject)
                        item2.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                        item2.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        item2.setForeground(QColor(255, 255, 255))
                        self.listWidget.addItem(item2)
                    else:
                        pass
                if rows == "G":
                    item = QTableWidgetItem(str(columns[qxr]))
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    item.setForeground(QColor(0, 0, 255))
                    if self.Asudokutable.item(18, qxr + 12) == None:
                        self.Asudokutable.setItem(18, qxr + 12, item)
                        stringObject = (
                            "Step: Put "
                            + str(columns[qxr])
                            + " in BR at r"
                            + str(7)
                            + "c"
                            + str(qxr + 1)
                        )
                        item2 = QListWidgetItem(stringObject)
                        item2.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                        item2.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        item2.setForeground(QColor(255, 255, 255))
                        self.listWidget.addItem(item2)
                    else:
                        pass
                if rows == "H":
                    item = QTableWidgetItem(str(columns[qxr]))
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    item.setForeground(QColor(0, 0, 255))
                    if self.Asudokutable.item(19, qxr + 12) == None:
                        self.Asudokutable.setItem(19, qxr + 12, item)
                        stringObject = (
                            "Step: Put "
                            + str(columns[qxr])
                            + " in BR at r"
                            + str(8)
                            + "c"
                            + str(qxr + 1)
                        )
                        item2 = QListWidgetItem(stringObject)
                        item2.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                        item2.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        item2.setForeground(QColor(255, 255, 255))
                        self.listWidget.addItem(item2)
                    else:
                        pass
                if rows == "I":
                    item = QTableWidgetItem(str(columns[qxr]))
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    item.setForeground(QColor(0, 0, 255))
                    if self.Asudokutable.item(20, qxr + 12) == None:
                        self.Asudokutable.setItem(20, qxr + 12, item)
                        stringObject = (
                            "Step: Put "
                            + str(columns[qxr])
                            + " in BR at r"
                            + str(9)
                            + "c"
                            + str(qxr + 1)
                        )
                        item2 = QListWidgetItem(stringObject)
                        item2.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                        item2.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        item2.setForeground(QColor(255, 255, 255))
                        self.listWidget.addItem(item2)
                    else:
                        pass
                Sudoku.t5 += 1

        if Sudoku.t1 >= 81:
            self.thread[0].stop()
        if Sudoku.t2 >= 81:
            self.thread[1].stop()
        if Sudoku.t3 >= 81:
            self.thread[2].stop()
        if Sudoku.t4 >= 81:
            self.thread[3].stop()
        if Sudoku.t5 >= 81:
            self.thread[4].stop()

    def getNameOfSudoku(self):
        for q in range(0, 100):
            for l in reader(open(file_path).readlines()[q * 22 : q * 22 + 1]):
                if l[0].endswith("Easy") and q < 20:
                    self.allsudoku.addItem(f"{q+1} Easy")
                if l[0].endswith("Moderate") and q < 40:
                    self.allsudoku.addItem(f"{q-19} Moderate")
                if l[0].endswith("Hard") and q < 60:
                    self.allsudoku.addItem(f"{q-39} Hard")
                if l[0].endswith("Fiendish") and q < 80:
                    self.allsudoku.addItem(f"{q-59} Fiendish")
                if l[0].endswith("Evil") and q < 100:
                    self.allsudoku.addItem(f"{q-79} Evil")

    def getsudoku(self):
        self.Asudokutable.setRowCount(0)
        current = self.allsudoku.currentIndex()
        x = 0
        self.Asudokutable.setRowCount(21)
        for l in reader(
            open(file_path).readlines()[(current) * 22 + 1 : (current) * 22 + 22]
        ):
            if l[0].isdecimal():
                item = QTableWidgetItem(str(l[0]))
                item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                item.setForeground(QColor(0, 0, 0))
                self.Asudokutable.setItem(x, 0, item)
            if l[1].isdecimal():
                item = QTableWidgetItem(str(l[1]))
                item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                item.setForeground(QColor(0, 0, 0))
                self.Asudokutable.setItem(x, 1, item)
            if l[2].isdecimal():
                item = QTableWidgetItem(str(l[2]))
                item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                item.setForeground(QColor(0, 0, 0))
                self.Asudokutable.setItem(x, 2, item)
            if l[3].isdecimal():
                item = QTableWidgetItem(str(l[3]))
                item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                item.setForeground(QColor(0, 0, 0))
                self.Asudokutable.setItem(x, 3, item)
            if l[4].isdecimal():
                item = QTableWidgetItem(str(l[4]))
                item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                item.setForeground(QColor(0, 0, 0))
                self.Asudokutable.setItem(x, 4, item)
            if l[5].isdecimal():
                item = QTableWidgetItem(str(l[5]))
                item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                item.setForeground(QColor(0, 0, 0))
                self.Asudokutable.setItem(x, 5, item)
            if l[6].isdecimal():
                item = QTableWidgetItem(str(l[6]))
                item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                item.setForeground(QColor(0, 0, 0))
                self.Asudokutable.setItem(x, 6, item)
            if l[7].isdecimal():
                item = QTableWidgetItem(str(l[7]))
                item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                item.setForeground(QColor(0, 0, 0))
                self.Asudokutable.setItem(x, 7, item)
            if l[8].isdecimal():
                item = QTableWidgetItem(str(l[8]))
                item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                item.setForeground(QColor(0, 0, 0))
                self.Asudokutable.setItem(x, 8, item)
            if l[9].isdecimal():
                item = QTableWidgetItem(str(l[9]))
                item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                item.setForeground(QColor(0, 0, 0))
                self.Asudokutable.setItem(x, 9, item)
            if l[10].isdecimal():
                item = QTableWidgetItem(str(l[10]))
                item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                item.setForeground(QColor(0, 0, 0))
                self.Asudokutable.setItem(x, 10, item)
            if l[11].isdecimal():
                item = QTableWidgetItem(str(l[11]))
                item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                item.setForeground(QColor(0, 0, 0))
                self.Asudokutable.setItem(x, 11, item)
            if l[12].isdecimal():
                item = QTableWidgetItem(str(l[12]))
                item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                item.setForeground(QColor(0, 0, 0))
                self.Asudokutable.setItem(x, 12, item)
            if l[13].isdecimal():
                item = QTableWidgetItem(str(l[13]))
                item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                item.setForeground(QColor(0, 0, 0))
                self.Asudokutable.setItem(x, 13, item)
            if l[14].isdecimal():
                item = QTableWidgetItem(str(l[14]))
                item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                item.setForeground(QColor(0, 0, 0))
                self.Asudokutable.setItem(x, 14, item)
            if l[15].isdecimal():
                item = QTableWidgetItem(str(l[15]))
                item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                item.setForeground(QColor(0, 0, 0))
                self.Asudokutable.setItem(x, 15, item)
            if l[16].isdecimal():
                item = QTableWidgetItem(str(l[16]))
                item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                item.setForeground(QColor(0, 0, 0))
                self.Asudokutable.setItem(x, 16, item)
            if l[17].isdecimal():
                item = QTableWidgetItem(str(l[17]))
                item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                item.setForeground(QColor(0, 0, 0))
                self.Asudokutable.setItem(x, 17, item)
            if l[18].isdecimal():
                item = QTableWidgetItem(str(l[18]))
                item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                item.setForeground(QColor(0, 0, 0))
                self.Asudokutable.setItem(x, 18, item)
            if l[19].isdecimal():
                item = QTableWidgetItem(str(l[19]))
                item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                item.setForeground(QColor(0, 0, 0))
                self.Asudokutable.setItem(x, 19, item)
            if l[20].isdecimal():
                item = QTableWidgetItem(str(l[20]))
                item.setTextAlignment(Qt.AlignCenter | Qt.AlignTop)
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                item.setForeground(QColor(0, 0, 0))
                self.Asudokutable.setItem(x, 20, item)
            x += 1

    def clearing(self):
        self.Asudokutable.setRowCount(0)
        self.Asudokutable.setRowCount(21)
        self.listWidget.clear()
        Sudoku.countdown=3600

    def settimerslider(self):
        a = QAbstractSlider.sliderPosition(self.timerCheck)
        if a == 0:
            self.timerframe.setGraphicsEffect(glory(opacity=1.0))
            QAbstractSlider.setSliderPosition(self.timerCheck, 1)
            self.timerCheck.setStyleSheet(
                "QSlider::groove:horizontal{border: 1px solid rgb(204, 204, 204);border-radius:15px;height: 30px; background:  rgb(54, 212, 73);}QSlider::handle:horizontal {image: url(:/Images/assets/icons/yes.png);width:30px;height:30px;min-width:30px;min-height:30px;max-width:30px;max-height:30px;border-radius: 15px;}"
            )
            self.start_worker_1()
        if a == 1:
            self.timerframe.setGraphicsEffect(glory(opacity=0.0))
            QAbstractSlider.setSliderPosition(self.timerCheck, 0)
            self.timerCheck.setStyleSheet(
                "QSlider::groove:horizontal{border: 1px solid rgb(204, 204, 204);border-radius:15px;height: 30px; background:  rgb(217, 217, 217);}QSlider::handle:horizontal {image: url(:/Images/assets/icons/no.png);width:30px;height:30px;min-width:30px;min-height:30px;max-width:30px;max-height:30px;border-radius: 15px;}"
            )
            self.stop_worker_1()

    def lcd_number(self, time):
        t = time
        mins, secs = divmod(t, 60)
        hours, mins = divmod(mins, 60)
        timer = "{:02d}:{:02d}:{:02d}".format(hours, mins, secs)
        self.timer.display(timer)
        Sudoku.countdown = t
        if Sudoku.countdown == 0:
            QMessageBox.about(
                self,
                "CountDown",
                '<p><span style="font-size:15pt; color:white; font-weight:600;">Your time is over.</span></p>',
            )
            self.thread[1].stop()
            Sudoku.countdown == 3600


if __name__ == "__main__":
    app = QApplication(argv)
    Form = Sudoku()
    Form.show()
    exit(app.exec_())
