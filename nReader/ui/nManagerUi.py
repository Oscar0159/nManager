# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets


class MainWindowUi(object):
    def setupUi(self, main_window):
        # main window
        main_window.setObjectName("MainWindow")
        main_window.setWindowTitle('nReader')
        main_window.setMinimumWidth(356)
        main_window.setMinimumHeight(600)
        main_window.resize(616, 900)

        # main vertical layout
        self.main_vlayout = QtWidgets.QVBoxLayout(main_window)

        # central widget
        self.centralwidget = QtWidgets.QWidget(main_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        # sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setLayout(self.main_vlayout)
        main_window.setCentralWidget(self.centralwidget)

        # top horizontal layout
        self.top_hlayout = QtWidgets.QHBoxLayout()
        self.main_vlayout.addLayout(self.top_hlayout)

        # top line editor
        self.searh_line = QtWidgets.QLineEdit()
        self.number_line = QtWidgets.QLineEdit()
        self.top_hlayout.addWidget(self.searh_line)
        self.top_hlayout.addWidget(self.number_line, alignment=QtCore.Qt.AlignRight)

        # top push button
        # self.dir_button = QtWidgets.QPushButton(icon=QtGui.QIcon(QtGui.QPixmap('./icon/folder_light.png')))
        self.zoomout_button = QtWidgets.QPushButton(icon=QtGui.QIcon(QtGui.QPixmap('./icon/zoom_out.png')))
        self.zoomin_button = QtWidgets.QPushButton(icon=QtGui.QIcon(QtGui.QPixmap('./icon/zoom_in.png')))
        # self.top_hlayout.addWidget(self.dir_button)
        self.top_hlayout.addWidget(self.zoomout_button)
        self.top_hlayout.addWidget(self.zoomin_button)

        # # top auto download check box
        # self.auto_download_box = QtWidgets.QCheckBox()
        # self.top_hlayout.addWidget(self.auto_download_box)
        #
        # # top auto download label
        # self.auto_download_label = QtWidgets.QLabel(text='自動下載')
        # self.top_hlayout.addWidget(self.auto_download_label)

        # pagination horizontal layout
        self.pagination_hlayout = QtWidgets.QHBoxLayout()
        self.main_vlayout.addLayout(self.pagination_hlayout)

        # pagination button
        self.add_pagination_button = QtWidgets.QPushButton(icon=QtGui.QIcon(QtGui.QPixmap('./icon/plus_light.png')))
        self.pagination_hlayout.addWidget(self.add_pagination_button, alignment=QtCore.Qt.AlignLeft)

        # main stack widget
        self.main_stack_widget = QtWidgets.QStackedWidget()
        self.main_vlayout.addWidget(self.main_stack_widget)


