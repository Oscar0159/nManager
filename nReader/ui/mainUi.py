# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWinExtras import QtWin


class UiMainWindow(object):
    def setupUi(self, MainWindow):
        # main window
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle('nReader')
        MainWindow.setMinimumWidth(400)
        MainWindow.setMinimumHeight(600)
        MainWindow.resize(600, 900)


        MainWindow.setWindowOpacity(0.95)

        # QLineEdit
        self.NumLineEdit = QtWidgets.QLineEdit()
        self.NumLineEdit.setObjectName('NumLineEdit')
        self.NumLineEdit.setValidator(QtGui.QIntValidator(1, 999999))
        self.NumLineEdit.setPlaceholderText('xxxxxx')
        self.NumLineEdit.setGeometry(0, 0, 151, 28)
        self.NumLineEdit.setAlignment(QtCore.Qt.AlignCenter)

        # QFormLayout
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.formLayout.setFormAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)

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
        self.hLayout.addWidget(self.NumLineEdit)
        self.hLayout.addWidget(self.checkButton)

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

