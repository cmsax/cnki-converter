# -*- coding: utf-8 -*-
# File: cnki-converter/main.py
# Author: MingshiCai i@unoiou.com
# Created Date: 2019-10-07 17:05:28
# ----
# Last Modified:
# Modified By:
# ----
# Copyright (c) 2019 MingshiCai i@unoiou.com
import sys
import time

from PySide2 import QtCore, QtWidgets, QtGui

from converter import converter


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.intro = "Drag CNKI file(s) here\nEndNote supported only"
        self.dump_path = ''

        self.setWindowTitle("Converter - by cms")
        self.setFixedSize(230, 120)

        self.text = QtWidgets.QLabel(self.intro)
        self.text.setAlignment(QtCore.Qt.AlignCenter)
        self.logo = QtWidgets.QLabel('🍉🐶🐒')
        self.logo.setStyleSheet('font-size: 20px')
        self.logo.setAlignment(QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.logo)
        self.layout.addWidget(self.text)

        self.setLayout(self.layout)

        self.setAcceptDrops(True)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

    def file_hover(self):
        self.text.setText('Oh yeah, put down')

    def file_unhover(self):
        self.text.setText(self.intro)

    def convert_file(self, filepath):
        try:
            self.dump_path = converter(filepath)
        except Exception as e:
            err = QtWidgets.QMessageBox(self)
            err.setIcon(QtWidgets.QMessageBox.Critical)
            err.setText('Is it an EndNote format text file?')
            err.setInformativeText(
                'You must drag an EndNote format reference file here.')
            err.setWindowTitle('Error')
            err.exec_()
        else:
            reply = QtWidgets.QMessageBox.information(
                self, 'Done', 'Converted file: {}'.format(self.dump_path), QtWidgets.QMessageBox.Ok)
        finally:
            self.file_unhover()

    def show_error(self):
        pass

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()
            self.file_hover()

    def dropEvent(self, e):
        urls = e.mimeData().urls()
        self.file_unhover()
        self.text.setText("converting, plz wait...")
        for index, url in enumerate(urls):
            self.convert_file(url.toLocalFile())

    def dragLeaveEvent(self, e):
        self.file_unhover()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = MyWidget()

    widget.show()

    sys.exit(app.exec_())
