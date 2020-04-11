# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QPoint, QRect, QSize, Qt
from PyQt5.QtWidgets import QLayout, QPushButton, QSizePolicy

# class PageWindow(QtWidgets.QMainWindow):
#     gotoSignal = QtCore.pyqtSignal(str)
#
#     def goto(self, name):
#         self.gotoSignal.emit(name)


class NormalUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # main window

        # main central widget
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        # main vertical layout
        self.main_vlayout = QtWidgets.QVBoxLayout()
        self.central_widget.setLayout(self.main_vlayout)

        # main scroll area
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.main_vlayout.addWidget(self.scroll_area)

        # group box in main scroll area
        self.group_box = QtWidgets.QGroupBox()
        self.scroll_area.setWidget(self.group_box)

        # flow layout in group box
        self.flow_layout = FlowLayout()
        self.group_box.setLayout(self.flow_layout)

        # main pagination horizontal layout
        self.pagination_hlayout = QtWidgets.QHBoxLayout()
        self.main_vlayout.addLayout(self.pagination_hlayout)

        # main page button
        self.first_button = QtWidgets.QPushButton(icon=QtGui.QIcon(QtGui.QPixmap('./icon/doubleLeft_light.png')))
        self.first_button.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed))
        self.previous_button = QtWidgets.QPushButton(icon=QtGui.QIcon(QtGui.QPixmap('./icon/left_light.png')))
        self.next_button = QtWidgets.QPushButton(icon=QtGui.QIcon(QtGui.QPixmap('./icon/right_light.png')))
        self.last_button = QtWidgets.QPushButton(icon=QtGui.QIcon(QtGui.QPixmap('./icon/doubleRight_light.png')))
        self.last_button.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed))
        self.pagination_hlayout.addWidget(self.first_button)
        self.pagination_hlayout.addWidget(self.previous_button, alignment=QtCore.Qt.AlignLeft)
        self.pagination_hlayout.addWidget(self.next_button, alignment=QtCore.Qt.AlignRight)
        self.pagination_hlayout.addWidget(self.last_button)


class GalleryUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        pass


class BookUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # main window

        # main central widget
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        # main vertical layout
        self.main_vlayout = QtWidgets.QVBoxLayout()
        self.central_widget.setLayout(self.main_vlayout)

        # main scroll area
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.main_vlayout.addWidget(self.scroll_area)

        # group box in main scroll area
        self.group_box = QtWidgets.QGroupBox()
        self.scroll_area.setWidget(self.group_box)

        # form layout in group box
        self.form_layout = QtWidgets.QFormLayout()
        self.group_box.setLayout(self.form_layout)

        # main pagination horizontal layout
        self.pagination_hlayout = QtWidgets.QHBoxLayout()
        self.main_vlayout.addLayout(self.pagination_hlayout)

        # main pagination
        self.first_button = QtWidgets.QPushButton(icon=QtGui.QIcon(QtGui.QPixmap('./icon/doubleLeft_light.png')))
        self.first_button.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed))
        self.previous_button = QtWidgets.QPushButton(icon=QtGui.QIcon(QtGui.QPixmap('./icon/left_light.png')))

        self.page_line = QtWidgets.QLineEdit()

        self.next_button = QtWidgets.QPushButton(icon=QtGui.QIcon(QtGui.QPixmap('./icon/right_light.png')))
        self.last_button = QtWidgets.QPushButton(icon=QtGui.QIcon(QtGui.QPixmap('./icon/doubleRight_light.png')))
        self.last_button.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed))
        self.pagination_hlayout.addWidget(self.first_button)
        self.pagination_hlayout.addWidget(self.previous_button, alignment=QtCore.Qt.AlignLeft)
        self.pagination_hlayout.addWidget(self.page_line)
        self.pagination_hlayout.addWidget(self.next_button, alignment=QtCore.Qt.AlignRight)
        self.pagination_hlayout.addWidget(self.last_button)


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

class UrlButton(QPushButton):
    def __init__(self, text: str, url: str):
        super(UrlButton, self).__init__(text=text)
        self.url = url

    def click(self) -> None:
        pass