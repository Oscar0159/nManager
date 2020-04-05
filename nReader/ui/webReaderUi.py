# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QPoint, QRect, QSize, Qt
from PyQt5.QtWidgets import (QApplication, QLayout, QPushButton, QSizePolicy,
        QWidget)
from PyQt5.QtWinExtras import QtWin


class UiMainWindow(object):
    def setupUi(self, MainWindow):
        # style
        with open('./ui/style.qss') as file:
            s = file.readline()
            #s = ''.join(s).strip('\n')
        MainWindow.setStyleSheet(s)

        # main window
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle('nReader')
        MainWindow.setMinimumWidth(400)
        MainWindow.setMinimumHeight(600)
        MainWindow.resize(600, 900)


        MainWindow.setWindowOpacity(0.95)
        #MainWindow.setWindowFlags(Qt.FramelessWindowHint)

        # QLineEdit
        self.NumLineEdit = QtWidgets.QLineEdit()
        self.NumLineEdit.setObjectName('NumLineEdit')
        self.NumLineEdit.setValidator(QtGui.QIntValidator(1, 999999))
        self.NumLineEdit.setPlaceholderText('xxxxxx')
        self.NumLineEdit.setGeometry(0, 0, 151, 28)
        self.NumLineEdit.setAlignment(QtCore.Qt.AlignCenter)

        # QFormLayout
        self.formLayout = FlowLayout()
        # self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        # self.formLayout.setRowWrapPolicy(QtWidgets.QFormLayout.DontWrapRows)

        # self.formLayout.setRowWrapPolicy(QtWidgets.QFormLayout.WrapLongRows)
        # self.formLayout.setLabelAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        # self.formLayout.setFormAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        # self.formLayout.setContentsMargins(0, 0, 0, 0)
        # pushSpacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        # self.formLayout.setItem(0, QtWidgets.QFormLayout.FieldRole, pushSpacerItem)

        # QGroupBox
        self.groupBox = QtWidgets.QGroupBox()
        self.groupBox.setLayout(self.formLayout)
        self.groupBox.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)

        # QScrollArea
        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setWidget(self.groupBox)
        self.scrollArea.setWidgetResizable(True)

        # QCheckBox
        self.checkButton = QtWidgets.QCheckBox('自動下載')


        # QPushButton
        self.downloadButton = QtWidgets.QPushButton()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.downloadButton.sizePolicy().hasHeightForWidth())
        self.downloadButton.setSizePolicy(sizePolicy)
        self.downloadButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap('./icon/zoom_out.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.downloadButton.setIcon(icon)

        self.downloadButton_1 = QtWidgets.QPushButton()
        self.downloadButton_1.setSizePolicy(sizePolicy)
        self.downloadButton_1.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap('./icon/zoom_in.ico'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.downloadButton_1.setIcon(icon)

        self.downloadButton_2 = QtWidgets.QPushButton()
        self.downloadButton_2.setSizePolicy(sizePolicy)
        self.downloadButton_2.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap('./icon/folder_light.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.downloadButton_2.setIcon(icon)

        # QHBoxLayout
        self.hLayout = QtWidgets.QHBoxLayout()
        self.hLayout.addWidget(self.downloadButton)
        self.hLayout.addWidget(self.downloadButton_1)
        self.hLayout.addWidget(self.downloadButton_2)
        spaceItem_L = QtWidgets.QSpacerItem(80, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        #self.hLayout.addItem(spaceItem_L)
        self.hLayout.addWidget(self.NumLineEdit)
        spaceItem_R = QtWidgets.QSpacerItem(80, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        #self.hLayout.addItem(spaceItem_R)
        self.hLayout.addWidget(self.checkButton)
        #self.hLayout.setStretch(3, 1)
        #self.hLayout.setStretch(4, )
        #self.hLayout.setStretch(5, 1)

        # QVBoxLayout
        self.vLayout = QtWidgets.QVBoxLayout()
        self.vLayout.addLayout(self.hLayout)
        self.vLayout.addWidget(self.scrollArea)

        # central widget
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setLayout(self.vLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        # menu
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 551, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "nReader"))

class FlowLayout(QLayout):
    def __init__(self, parent=None, margin=0, spacing=-1):
        super(FlowLayout, self).__init__(parent)

        if parent is not None:
            self.setContentsMargins(margin, margin, margin, margin)

        self.setSpacing(spacing)

        self.itemList = []

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, item):
        self.itemList.append(item)

    def count(self):
        return len(self.itemList)

    def itemAt(self, index):
        if index >= 0 and index < len(self.itemList):
            return self.itemList[index]

        return None

    def takeAt(self, index):
        if index >= 0 and index < len(self.itemList):
            return self.itemList.pop(index)

        return None

    def expandingDirections(self):
        return Qt.Orientations(Qt.Orientation(0))

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        height = self.doLayout(QRect(0, 0, width, 0), True)
        return height

    def setGeometry(self, rect):
        super(FlowLayout, self).setGeometry(rect)
        self.doLayout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()

        for item in self.itemList:
            size = size.expandedTo(item.minimumSize())

        margin, _, _, _ = self.getContentsMargins()

        size += QSize(2 * margin, 2 * margin)
        return size

    def doLayout(self, rect, testOnly):
        x = rect.x()
        y = rect.y()
        lineHeight = 0

        for item in self.itemList:
            wid = item.widget()
            spaceX = self.spacing() + wid.style().layoutSpacing(QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Horizontal)
            spaceY = self.spacing() + wid.style().layoutSpacing(QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Vertical)
            nextX = x + item.sizeHint().width() + spaceX
            if nextX - spaceX > rect.right() and lineHeight > 0:
                x = rect.x()
                y = y + lineHeight + spaceY
                nextX = x + item.sizeHint().width() + spaceX
                lineHeight = 0

            if not testOnly:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

            x = nextX
            lineHeight = max(lineHeight, item.sizeHint().height())

        return y + lineHeight - rect.y()

# MainWindow.setLayout(self.layout)
# QtCore.QMetaObject.connectSlotsByName(MainWindow)
# MainWindow.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
# MainWindow.setAttribute(Qt.WA_NoSystemBackground, True)
# MainWindow.setAttribute(Qt.WA_TranslucentBackground, True)
# MainWindow.resized.connect(self.say)

