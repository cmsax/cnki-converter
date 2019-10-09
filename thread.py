import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class ProcessRunnable(QRunnable):
    def __init__(self, target, args):
        QRunnable.__init__(self)
        self.t = target
        self.args = args

    def run(self):
        self.t(*self.args)

    def start(self):
        QThreadPool.globalInstance().start(self)


def run(user_input, log):
    text = ""
    if user_input == "":
        text = "Please enter a value\n"
    else:
        text = "Test"

    QMetaObject.invokeMethod(log,
                             "append", Qt.QueuedConnection,
                             Q_ARG(str, text))


class LogginOutput(QTextEdit):
    def __init__(self, parent=None):
        super(LogginOutput, self).__init__(parent)

        self.setReadOnly(True)
        self.setLineWrapMode(self.NoWrap)
        self.insertPlainText("")

    @pyqtSlot(str)
    def append(self, text):
        self.moveCursor(QTextCursor.End)
        current = self.toPlainText()

        if current == "":
            self.insertPlainText(text)
        else:
            self.insertPlainText("\n" + text)

        sb = self.verticalScrollBar()
        sb.setValue(sb.maximum())


class App(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        label = QLabel('Amount')
        amount_input = QLineEdit()
        submit = QPushButton('Submit', self)
        box = LogginOutput(self)

        submit.clicked.connect(lambda: self.changeLabel(box, amount_input))

        grid = QGridLayout()
        grid.addWidget(label, 0, 0)
        grid.addWidget(amount_input, 1, 0)
        grid.addWidget(submit, 1, 1)
        grid.addWidget(box, 2, 0, 5, 2)

        self.setLayout(grid)
        self.resize(350, 250)
        self.setWindowTitle('GetMeStuff Bot v0.1')
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def changeLabel(self, box, user_input):
        self.p = ProcessRunnable(
            target=run, args=(user_input.displayText(), box))
        self.p.start()
        user_input.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = App()
    sys.exit(app.exec_())
