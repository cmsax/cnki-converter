from PySide2 import QtWidgets


class AboutWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("About")
        self.text = QtWidgets.QLabel("fuck")
        self.ok = QtWidgets.QPushButton("fuck")
        self.ok.setText("ok")
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.ok)
        self.setLayout(self.layout)
