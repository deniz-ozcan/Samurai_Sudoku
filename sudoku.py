from PyQt5.QtWidgets import (
    QWidget,
    QSizePolicy,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QGridLayout,
    QComboBox,
    QTableWidget,
    QAbstractItemView,
    QListWidget,
    QListView,
    QSlider,
    QLCDNumber,

)

from PyQt5.QtGui import (
    QPixmap,
    QIcon,
    QFont,
    
)
from PyQt5.QtCore import (
    Qt,
    QSize,
    QCoreApplication,
    QMetaObject,
    QRect,
    
)


class Ui_sudoku(object):
    def setupUi(self, sudoku):
        sudoku.setObjectName("sudoku")
        sudoku.resize(1366, 730)
        sudoku.setMaximumSize(QSize(16777211, 16777215))
        icon = QIcon()
        icon.addPixmap(QPixmap(":/Images/assets/icons/windowicon.png"), QIcon.Normal, QIcon.Off)
        sudoku.setWindowIcon(icon)
        sudoku.setStyleSheet("#timepush,#confpush{\n"
"    border-radius:17px;\n"
"    border:2px solid rgb(150, 150, 150);\n"
"    background:transparent;\n"
"}\n"
"\n"
"#lastFrame{\n"
"    background-color: rgba(24, 24, 36,255);\n"
"    border-radius:30px;\n"
"    border: 3px solid rgb(230, 5, 64);\n"
"}\n"
"#suwidget{\n"
"    border-top:3px solid  rgb(213, 30, 1);\n"
"    border-left:3px solid  rgb(213, 30, 1);\n"
"    border-bottom:2px solid  rgb(213, 30, 1);\n"
"    border-right:2px solid  rgb(213, 30, 1);\n"
"    background:white;\n"
"}\n"
"\n"
"QWidget {\n"
"    background-color:transparent;\n"
"    border:none;\n"
"\n"
"}\n"
"QTableWidget {\n"
"    gridline-color: rgb(230, 5, 64);\n"
"}\n"
"QLabel#bottomlabel,#rightlabel,#toplabel,#leftlabel{\n"
"    background-color:white;\n"
"}\n"
"QLabel#grl1,#grl2,#grl3,#grl4,#grl5,#grl6,#grl7,#grl8,#grl9,#grl90,#grl91,#grl92{\n"
"    border:2px solid rgb(230, 5, 64);\n"
"    background-color:white;\n"
"}\n"
"#whiteFrame,#buttonFrame{\n"
"    background:white;\n"
"    border-radius:30px;\n"
"}\n"
"#titleLabel{\n"
"    image:url(:/Images/assets/icons/background.png);\n"
"}\n"
"#headerFrame{\n"
"    border-bottom: 3px solid rgb(230, 5, 64);\n"
"}")
        self.lastFrame = QFrame(sudoku)
        self.lastFrame.setGeometry(QRect(243, 35, 945, 620))
        self.lastFrame.setMinimumSize(QSize(945, 620))
        self.lastFrame.setMaximumSize(QSize(945, 620))
        self.lastFrame.setStyleSheet("")
        self.lastFrame.setFrameShape(QFrame.StyledPanel)
        self.lastFrame.setFrameShadow(QFrame.Raised)
        self.lastFrame.setObjectName("lastFrame")
        self.verticalLayout = QVBoxLayout(self.lastFrame)
        self.verticalLayout.setContentsMargins(0, 0, 0, 24)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.headerFrame = QFrame(self.lastFrame)
        self.headerFrame.setMinimumSize(QSize(945, 50))
        self.headerFrame.setMaximumSize(QSize(945, 50))
        self.headerFrame.setStyleSheet("")
        self.headerFrame.setFrameShape(QFrame.StyledPanel)
        self.headerFrame.setFrameShadow(QFrame.Raised)
        self.headerFrame.setObjectName("headerFrame")
        self.horizontalLayout_2 = QHBoxLayout(self.headerFrame)
        self.horizontalLayout_2.setContentsMargins(0, 0, 10, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.titleLabel = QLabel(self.headerFrame)
        self.titleLabel.setMinimumSize(QSize(810, 35))
        self.titleLabel.setMaximumSize(QSize(810, 35))
        self.titleLabel.setText("")
        self.titleLabel.setObjectName("titleLabel")
        self.horizontalLayout_2.addWidget(self.titleLabel, 0, Qt.AlignVCenter)
        self.minimize = QPushButton(self.headerFrame)
        self.minimize.setText("")
        icon1 = QIcon()
        icon1.addPixmap(QPixmap(":/Images/assets/icons/arrow-down-left.svg"), QIcon.Normal, QIcon.Off)
        self.minimize.setIcon(icon1)
        self.minimize.setIconSize(QSize(20, 20))
        self.minimize.setObjectName("minimize")
        self.horizontalLayout_2.addWidget(self.minimize, 0, Qt.AlignVCenter)
        self.closeBut = QPushButton(self.headerFrame)
        self.closeBut.setText("")
        icon2 = QIcon()
        icon2.addPixmap(QPixmap(":/Images/assets/icons/x.svg"), QIcon.Normal, QIcon.Off)
        self.closeBut.setIcon(icon2)
        self.closeBut.setIconSize(QSize(20, 20))
        self.closeBut.setObjectName("closeBut")
        self.horizontalLayout_2.addWidget(self.closeBut, 0, Qt.AlignVCenter)
        self.verticalLayout.addWidget(self.headerFrame, 0, Qt.AlignTop)
        self.frame_2 = QFrame(self.lastFrame)
        self.frame_2.setMinimumSize(QSize(945, 531))
        self.frame_2.setMaximumSize(QSize(945, 531))
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_6 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.whiteFrame = QFrame(self.frame_2)
        self.whiteFrame.setMinimumSize(QSize(531, 531))
        self.whiteFrame.setMaximumSize(QSize(531, 531))
        self.whiteFrame.setStyleSheet("")
        self.whiteFrame.setFrameShape(QFrame.StyledPanel)
        self.whiteFrame.setFrameShadow(QFrame.Raised)
        self.whiteFrame.setObjectName("whiteFrame")
        self.horizontalLayout = QHBoxLayout(self.whiteFrame)
        self.horizontalLayout.setContentsMargins(20, 20, 20, 20)
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.suwidget = QWidget(self.whiteFrame)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.suwidget.sizePolicy().hasHeightForWidth())
        self.suwidget.setSizePolicy(sizePolicy)
        self.suwidget.setMinimumSize(QSize(488, 488))
        self.suwidget.setMaximumSize(QSize(488, 488))
        font = QFont()
        font.setPointSize(8)
        self.suwidget.setFont(font)
        self.suwidget.setStyleSheet("")
        self.suwidget.setObjectName("suwidget")
        self.leftlabel = QLabel(self.suwidget)
        self.leftlabel.setGeometry(QRect(0, 210, 140, 68))
        self.leftlabel.setMinimumSize(QSize(138, 68))
        self.leftlabel.setText("")
        self.leftlabel.setObjectName("leftlabel")
        self.rightlabel = QLabel(self.suwidget)
        self.rightlabel.setGeometry(QRect(350, 210, 138, 68))
        self.rightlabel.setText("")
        self.rightlabel.setObjectName("rightlabel")
        self.bottomlabel = QLabel(self.suwidget)
        self.bottomlabel.setGeometry(QRect(210, 350, 68, 138))
        self.bottomlabel.setText("")
        self.bottomlabel.setObjectName("bottomlabel")
        self.toplabel = QLabel(self.suwidget)
        self.toplabel.setGeometry(QRect(210, 0, 68, 138))
        self.toplabel.setText("")
        self.toplabel.setObjectName("toplabel")
        self.grl1 = QLabel(self.suwidget)
        self.grl1.setGeometry(QRect(70, 3, 3, 482))
        self.grl1.setStyleSheet("")
        self.grl1.setText("")
        self.grl1.setObjectName("grl1")
        self.grl2 = QLabel(self.suwidget)
        self.grl2.setGeometry(QRect(140, 3, 3, 482))
        self.grl2.setStyleSheet("")
        self.grl2.setText("")
        self.grl2.setObjectName("grl2")
        self.grl3 = QLabel(self.suwidget)
        self.grl3.setGeometry(QRect(207, 3, 3, 482))
        self.grl3.setStyleSheet("")
        self.grl3.setText("")
        self.grl3.setObjectName("grl3")
        self.grl4 = QLabel(self.suwidget)
        self.grl4.setGeometry(QRect(278, 3, 3, 482))
        self.grl4.setStyleSheet("")
        self.grl4.setText("")
        self.grl4.setObjectName("grl4")
        self.grl5 = QLabel(self.suwidget)
        self.grl5.setGeometry(QRect(347, 3, 3, 482))
        self.grl5.setStyleSheet("")
        self.grl5.setText("")
        self.grl5.setObjectName("grl5")
        self.grl6 = QLabel(self.suwidget)
        self.grl6.setGeometry(QRect(414, 3, 3, 482))
        self.grl6.setStyleSheet("")
        self.grl6.setText("")
        self.grl6.setObjectName("grl6")
        self.grl7 = QLabel(self.suwidget)
        self.grl7.setGeometry(QRect(3, 70, 482, 3))
        self.grl7.setStyleSheet("")
        self.grl7.setText("")
        self.grl7.setObjectName("grl7")
        self.grl8 = QLabel(self.suwidget)
        self.grl8.setGeometry(QRect(3, 138, 482, 3))
        self.grl8.setStyleSheet("")
        self.grl8.setText("")
        self.grl8.setObjectName("grl8")
        self.grl9 = QLabel(self.suwidget)
        self.grl9.setGeometry(QRect(3, 207, 482, 3))
        self.grl9.setStyleSheet("")
        self.grl9.setText("")
        self.grl9.setObjectName("grl9")
        self.grl90 = QLabel(self.suwidget)
        self.grl90.setGeometry(QRect(3, 278, 482, 3))
        self.grl90.setStyleSheet("")
        self.grl90.setText("")
        self.grl90.setObjectName("grl90")
        self.grl91 = QLabel(self.suwidget)
        self.grl91.setGeometry(QRect(3, 347, 482, 3))
        self.grl91.setStyleSheet("")
        self.grl91.setText("")
        self.grl91.setObjectName("grl91")
        self.grl92 = QLabel(self.suwidget)
        self.grl92.setGeometry(QRect(3, 416, 482, 3))
        self.grl92.setStyleSheet("")
        self.grl92.setText("")
        self.grl92.setObjectName("grl92")
        self.Asudokutable = QTableWidget(self.suwidget)
        self.Asudokutable.setGeometry(QRect(3, 3, 486, 486))
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Asudokutable.sizePolicy().hasHeightForWidth())
        self.Asudokutable.setSizePolicy(sizePolicy)
        self.Asudokutable.setMinimumSize(QSize(486, 486))
        self.Asudokutable.setMaximumSize(QSize(486, 486))
        font = QFont()
        font.setPointSize(15)
        self.Asudokutable.setFont(font)
        self.Asudokutable.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.Asudokutable.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.Asudokutable.setAutoScroll(False)
        self.Asudokutable.setTabKeyNavigation(False)
        self.Asudokutable.setProperty("showDropIndicator", False)
        self.Asudokutable.setDragDropOverwriteMode(False)
        self.Asudokutable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.Asudokutable.setTextElideMode(Qt.ElideMiddle)
        self.Asudokutable.setGridStyle(Qt.CustomDashLine)
        self.Asudokutable.setWordWrap(False)
        self.Asudokutable.setCornerButtonEnabled(False)
        self.Asudokutable.setRowCount(21)
        self.Asudokutable.setColumnCount(21)
        self.Asudokutable.setObjectName("Asudokutable")
        self.Asudokutable.horizontalHeader().setVisible(False)
        self.Asudokutable.horizontalHeader().setCascadingSectionResizes(True)
        self.Asudokutable.horizontalHeader().setDefaultSectionSize(23)
        self.Asudokutable.horizontalHeader().setMinimumSectionSize(23)
        self.Asudokutable.verticalHeader().setVisible(False)
        self.Asudokutable.verticalHeader().setCascadingSectionResizes(True)
        self.Asudokutable.verticalHeader().setDefaultSectionSize(23)
        self.Asudokutable.raise_()
        self.grl92.raise_()
        self.grl91.raise_()
        self.grl90.raise_()
        self.grl9.raise_()
        self.grl8.raise_()
        self.grl7.raise_()
        self.grl6.raise_()
        self.grl5.raise_()
        self.grl4.raise_()
        self.grl3.raise_()
        self.grl2.raise_()
        self.grl1.raise_()
        self.leftlabel.raise_()
        self.toplabel.raise_()
        self.rightlabel.raise_()
        self.bottomlabel.raise_()
        self.horizontalLayout.addWidget(self.suwidget)
        self.horizontalLayout_6.addWidget(self.whiteFrame)
        self.buttonFrame = QFrame(self.frame_2)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonFrame.sizePolicy().hasHeightForWidth())
        self.buttonFrame.setSizePolicy(sizePolicy)
        self.buttonFrame.setMinimumSize(QSize(325, 531))
        self.buttonFrame.setMaximumSize(QSize(325, 531))
        self.buttonFrame.setStyleSheet("QPushButton{\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgba(255, 0, 0, 255), stop:1 rgba(0, 0, 255, 255));\n"
"    color:rgba(255, 255, 255, 255);\n"
"    border-radius:15px;\n"
"    font-size:13pt;\n"
"    width:156px;\n"
"    height:30px;\n"
"    min-width:156px;\n"
"    min-height:30px;\n"
"    max-width:156px;\n"
"    max-height:30px;\n"
"}\n"
"#checkFrame{\n"
"    border-radius:15px;\n"
"    background-color:qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgba(255, 0, 0, 255), stop:1 rgba(0, 0, 255, 255));\n"
"    width:310px;\n"
"    height:40px;\n"
"    min-width:310px;\n"
"    min-height:40px;\n"
"    max-width:263px;\n"
"    max-height:40px;\n"
"}\n"
"\n"
"QLabel{\n"
"    color:white;\n"
"\n"
"}\n"
"QPushButton:hover{\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(150, 123, 111, 219), stop:1 rgba(85, 81, 84, 226));\n"
"}\n"
"QPushButton:pressed{\n"
"    padding-left:5px;\n"
"    padding-top:5px;\n"
"    background-color:rgba(150, 123, 111, 255);\n"
"}\n"
"QLineEdit{\n"
"    background: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgba(255, 0, 0, 255), stop:1 rgba(0, 0, 255, 255));\n"
"    border-radius:20px;\n"
"    color:rgb(255,255,255);\n"
"    padding-left:10px;\n"
"    padding-top:10px;\n"
"}\n"
"\n"
"\n"
"QAbstractItemView {\n"
"    border-top:5px solid qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgba(255, 0, 0, 255), stop:1 rgba(0, 0, 255, 255));\n"
"    border-left:5px solid  rgba(255, 0, 0, 255);\n"
"    border-right:5px solid  rgba(0, 0, 255, 255);\n"
"    border-bottom:5px solid qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgba(255, 0, 0, 255), stop:1 rgba(0, 0, 255, 255));\n"
"    padding: 5 5 16 5;\n"
"    background-color:qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgba(255, 0, 0, 255), stop:1 rgba(0, 0, 255, 255));\n"
"    color: #ffffff;\n"
"}\n"
"QComboBox {\n"
"    background: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgba(255, 0, 0, 255), stop:1 rgba(0, 0, 255, 255));\n"
"    border-radius:20px;\n"
"    color:rgb(255,255,255);\n"
"    padding-left:10px;\n"
"\n"
"}\n"
"QScrollBar:vertical {\n"
"border-radius: 5px;\n"
"background:qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(255, 255, 255, 255));\n"
"width:10px;\n"
"margin: 0px 0px 0px 0px;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical {\n"
"border-radius: 5px;\n"
"background: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgba(255, 0, 0, 255), stop:1 rgba(0, 0, 255, 255));\n"
"    min-width:10px;\n"
"    max-width:10px;\n"
"    min-height:10px;\n"
"    max-height:10px;\n"
"}\n"
"QScrollBar::add-line:vertical {\n"
"height: 0px;\n"
"subcontrol-position: bottom;\n"
"subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::sub-line:vertical {\n"
"height: 0px;\n"
"subcontrol-position: top;\n"
"subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"background:transparent;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: url(:/Images/assets/icons/caret-circle-down .png);\n"
"    min-width:20px;\n"
"    max-width:20px;\n"
"    min-height:20px;\n"
"    max-height:20px;\n"
"    margin-right:2px;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    border:none;\n"
"    background:transparent;\n"
"}\n"
"\n"
"#timer{\n"
"    background-color:qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgba(255, 0, 0, 255), stop:1 rgba(0, 0, 255, 255));\n"
"    border-radius:15px;\n"
"    color:white;\n"
"}")
        self.buttonFrame.setFrameShape(QFrame.StyledPanel)
        self.buttonFrame.setFrameShadow(QFrame.Raised)
        self.buttonFrame.setObjectName("buttonFrame")
        self.gridLayout = QGridLayout(self.buttonFrame)
        self.gridLayout.setContentsMargins(9, 5, -1, 5)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.listWidget = QListWidget(self.buttonFrame)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy)
        self.listWidget.setMinimumSize(QSize(310, 150))
        self.listWidget.setMaximumSize(QSize(310, 150))
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.listWidget.setFont(font)
        self.listWidget.setStyleSheet("QAbstractItemView {\n"
"    border:none;\n"
"    border-radius:20px;\n"
"    padding: 5 5 16 5;\n"
"    background-color:qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgba(255, 0, 0, 255), stop:1 rgba(0, 0, 255, 255));\n"
"    color: #ffffff;\n"
"    padding:10px;\n"
"}\n"
"QScrollBar:vertical {\n"
"border-radius: 5px;\n"
"background:qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(255, 255, 255, 255));\n"
"width:10px;\n"
"margin: 0px 0px 0px 0px;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical {\n"
"border-radius: 5px;\n"
"background: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgba(255, 0, 0, 255), stop:1 rgba(0, 0, 255, 255));\n"
"    min-width:10px;\n"
"    max-width:10px;\n"
"    min-height:10px;\n"
"    max-height:10px;\n"
"}\n"
"QScrollBar::add-line:vertical {\n"
"height: 0px;\n"
"subcontrol-position: bottom;\n"
"subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::sub-line:vertical {\n"
"height: 0px;\n"
"subcontrol-position: top;\n"
"subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"background:transparent;\n"
"}")
        self.listWidget.setEditTriggers(QAbstractItemView.AllEditTriggers)
        self.listWidget.setViewMode(QListView.ListMode)
        self.listWidget.setObjectName("listWidget")
        self.gridLayout.addWidget(self.listWidget, 5, 0, 1, 2, Qt.AlignHCenter)
        self.checkFrame = QFrame(self.buttonFrame)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkFrame.sizePolicy().hasHeightForWidth())
        self.checkFrame.setSizePolicy(sizePolicy)
        self.checkFrame.setMinimumSize(QSize(310, 40))
        self.checkFrame.setMaximumSize(QSize(263, 40))
        self.checkFrame.setStyleSheet("")
        self.checkFrame.setFrameShape(QFrame.StyledPanel)
        self.checkFrame.setFrameShadow(QFrame.Raised)
        self.checkFrame.setObjectName("checkFrame")
        self.horizontalLayout_3 = QHBoxLayout(self.checkFrame)
        self.horizontalLayout_3.setContentsMargins(90, 0, 90, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.timerlabel = QLabel(self.checkFrame)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.timerlabel.sizePolicy().hasHeightForWidth())
        self.timerlabel.setSizePolicy(sizePolicy)
        self.timerlabel.setMinimumSize(QSize(50, 0))
        self.timerlabel.setMaximumSize(QSize(50, 16777215))
        font = QFont()
        font.setPointSize(13)
        self.timerlabel.setFont(font)
        self.timerlabel.setObjectName("timerlabel")
        self.horizontalLayout_3.addWidget(self.timerlabel)
        self.timerCheck = QSlider(self.checkFrame)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.timerCheck.sizePolicy().hasHeightForWidth())
        self.timerCheck.setSizePolicy(sizePolicy)
        self.timerCheck.setMinimumSize(QSize(60, 32))
        self.timerCheck.setMaximumSize(QSize(60, 32))
        self.timerCheck.setStyleSheet("QSlider::groove:horizontal {\n"
"    border-radius:15px;\n"
"    height: 30px; \n"
"    background:  rgb(217, 217, 217);\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"    image: url(:/Images/assets/icons/no.png);\n"
"    width:30px;\n"
"    height:30px;\n"
"    min-width:30px;\n"
"    min-height:30px;\n"
"    max-width:30px;\n"
"    max-height:30px;\n"
"    border-radius: 15px;\n"
"}")
        self.timerCheck.setMaximum(1)
        self.timerCheck.setPageStep(1)
        self.timerCheck.setOrientation(Qt.Horizontal)
        self.timerCheck.setInvertedAppearance(False)
        self.timerCheck.setInvertedControls(False)
        self.timerCheck.setObjectName("timerCheck")
        self.horizontalLayout_3.addWidget(self.timerCheck)
        self.gridLayout.addWidget(self.checkFrame, 14, 0, 1, 1, Qt.AlignHCenter)
        self.timerframe = QFrame(self.buttonFrame)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.timerframe.sizePolicy().hasHeightForWidth())
        self.timerframe.setSizePolicy(sizePolicy)
        self.timerframe.setMinimumSize(QSize(310, 60))
        self.timerframe.setMaximumSize(QSize(310, 60))
        self.timerframe.setFrameShape(QFrame.StyledPanel)
        self.timerframe.setFrameShadow(QFrame.Raised)
        self.timerframe.setObjectName("timerframe")
        self.horizontalLayout_4 = QHBoxLayout(self.timerframe)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.timer = QLCDNumber(self.timerframe)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.timer.sizePolicy().hasHeightForWidth())
        self.timer.setSizePolicy(sizePolicy)
        self.timer.setMinimumSize(QSize(310, 60))
        self.timer.setMaximumSize(QSize(310, 60))
        font = QFont()
        font.setPointSize(8)
        self.timer.setFont(font)
        self.timer.setDigitCount(8)
        self.timer.setProperty("intValue", 0)
        self.timer.setObjectName("timer")
        self.horizontalLayout_4.addWidget(self.timer)
        self.gridLayout.addWidget(self.timerframe, 15, 0, 1, 2)
        self.allsudoku = QComboBox(self.buttonFrame)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.allsudoku.sizePolicy().hasHeightForWidth())
        self.allsudoku.setSizePolicy(sizePolicy)
        self.allsudoku.setMinimumSize(QSize(310, 40))
        self.allsudoku.setMaximumSize(QSize(150, 40))
        font = QFont()
        font.setPointSize(15)
        self.allsudoku.setFont(font)
        self.allsudoku.setObjectName("allsudoku")
        self.gridLayout.addWidget(self.allsudoku, 0, 0, 1, 1, Qt.AlignHCenter)
        self.LoadButton = QPushButton(self.buttonFrame)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LoadButton.sizePolicy().hasHeightForWidth())
        self.LoadButton.setSizePolicy(sizePolicy)
        self.LoadButton.setMinimumSize(QSize(156, 30))
        self.LoadButton.setMaximumSize(QSize(156, 30))
        self.LoadButton.setObjectName("LoadButton")
        self.gridLayout.addWidget(self.LoadButton, 1, 0, 1, 1)
        self.solveButton = QPushButton(self.buttonFrame)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.solveButton.sizePolicy().hasHeightForWidth())
        self.solveButton.setSizePolicy(sizePolicy)
        self.solveButton.setMinimumSize(QSize(156, 30))
        self.solveButton.setMaximumSize(QSize(156, 30))
        self.solveButton.setObjectName("solveButton")
        self.gridLayout.addWidget(self.solveButton, 1, 1, 1, 1)
        self.restartButton = QPushButton(self.buttonFrame)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.restartButton.sizePolicy().hasHeightForWidth())
        self.restartButton.setSizePolicy(sizePolicy)
        self.restartButton.setMinimumSize(QSize(310, 40))
        self.restartButton.setMaximumSize(QSize(310, 40))
        self.restartButton.setStyleSheet("QPushButton{\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgba(255, 0, 0, 255), stop:1 rgba(0, 0, 255, 255));\n"
"    color:rgba(255, 255, 255, 255);\n"
"    border-radius:15px;\n"
"    font-size:13pt;\n"
"    width:310px;\n"
"    height:40px;\n"
"    min-width:310px;\n"
"    min-height:40px;\n"
"    max-width:310px;\n"
"    max-height:40px;\n"
"}\n"
"QPushButton:hover{\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(150, 123, 111, 219), stop:1 rgba(85, 81, 84, 226));\n"
"}\n"
"QPushButton:pressed{\n"
"    padding-left:5px;\n"
"    padding-top:5px;\n"
"    background-color:rgba(150, 123, 111, 255);\n"
"}")
        self.restartButton.setObjectName("restartButton")
        self.gridLayout.addWidget(self.restartButton, 2, 0, 1, 1)
        self.horizontalLayout_6.addWidget(self.buttonFrame)
        self.verticalLayout.addWidget(self.frame_2, 0, Qt.AlignHCenter)
        self.timepush = QPushButton(sudoku)
        self.timepush.setGeometry(QRect(994, 480, 62, 34))
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.timepush.sizePolicy().hasHeightForWidth())
        self.timepush.setSizePolicy(sizePolicy)
        self.timepush.setMinimumSize(QSize(62, 34))
        self.timepush.setMaximumSize(QSize(62, 34))
        self.timepush.setStyleSheet("")
        self.timepush.setText("")
        self.timepush.setObjectName("timepush")

        self.retranslateUi(sudoku)
        QMetaObject.connectSlotsByName(sudoku)

    def retranslateUi(self, sudoku):
        _translate = QCoreApplication.translate
        sudoku.setWindowTitle(_translate("sudoku", "Sudoku"))
        self.timerlabel.setText(_translate("sudoku", "Timer:"))
        self.LoadButton.setToolTip(_translate("sudoku", "<html><head/><body><p><span style=\" font-size:12pt;\">First pick one of sudokus, and press the Load button for the Sudoku.</span></p></body></html>"))
        self.LoadButton.setText(_translate("sudoku", "Load"))
        self.solveButton.setToolTip(_translate("sudoku", "<html><head/><body><p><span style=\" font-size:12pt;\">Sometimes, press the Solve button more than once for the solution.</span></p></body></html>"))
        self.solveButton.setText(_translate("sudoku", "Solve"))
        self.restartButton.setText(_translate("sudoku", "Restart"))
import res_rc_rc
