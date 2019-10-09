from PySide2 import QtCore, QtWidgets


class DragDrop(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__()
        self.icon = QtWidgets.QLabel("+")
        self.icon.setAlignment(QtCore.Qt.AlignCenter)

        self.setFixedSize(300, 300)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.icon)

        self.setStyleSheet("background-color: #042054")

        self.setAcceptDrops(True)
        self.show()

    def dragEnterEvent(self, e):
        print('enter')

    def dragLeaveEvent(self, e):
        print('leave')

    def dropEvent(self, e):
        print('drop')
