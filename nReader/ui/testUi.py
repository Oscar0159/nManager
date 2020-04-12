from PyQt5 import QtWidgets, QtCore, QtGui

class MainWindowUi(object):
    def setup(self, main_window):
        main_window.setObjectName("MainWindow")
        main_window.setWindowTitle('test')
        main_window.setMinimumWidth(400)
        main_window.setMinimumHeight(600)
        main_window.resize(600, 900)

        # main central widget
        self.central_widget = QtWidgets.QWidget()
        main_window.setCentralWidget(self.central_widget)

        # main vertical layout
        self.main_vlayout = QtWidgets.QVBoxLayout(self.central_widget)

        # add button
        self.add_button = QtWidgets.QPushButton('Add!')
        self.add_button.setObjectName('addButton')
        self.main_vlayout.addWidget(self.add_button)

        QtCore.QMetaObject.connectSlotsByName(main_window)
