# -*- coding: utf-8 -*-
# File: cnki-converter/main.py
# Author: MingshiCai i@unoiou.com
# Created Date: 2019-10-07 17:05:28
# ----
# Last Modified:
# Modified By:
# ----
# Copyright (c) 2019 MingshiCai i@unoiou.com
"""
1. `print` is thread safe, use `print` instead of `logging`.
2. QRunnable object will be deleted, Internal C++ object, after ran if it's un-referenced.
"""
import sys

from PySide2 import QtCore, QtWidgets

from converter import converter
# from update import Updater


class ConverterSignals(QtCore.QObject):
    finished = QtCore.Signal()
    result = QtCore.Signal(object)


class Converter(QtCore.QRunnable):
    def __init__(self, files=[]):
        super(Converter, self).__init__()
        self.signals = ConverterSignals()
        self.files = files
        self.result = {
            'files_count': len(self.files),
            'suc_count': 0, 'dump_file_paths': [], 'entries_count': 0,
            'exceptions': []
        }

    def run(self):
        for filepath in self.files:
            try:
                dump, count = converter(filepath)
            except Exception as e:
                self.result['exceptions'].append(str(e))
            else:
                self.result['suc_count'] += 1
                self.result['dump_file_paths'].append(dump)
                self.result['entries_count'] += count
            finally:
                self.signals.finished.emit()

        self.signals.result.emit(self.result)

    def start(self):
        QtCore.QThreadPool.globalInstance().start(self)


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.intro = "Drag CNKI file(s) here.\nEndNote supported only."
        self.waiting_logo_content = "🐒"
        self.hover_logo_content = "👇"
        self.running_logo_content = "👍"

        self.dump_path = ''
        self.item_count = 0

        self.setWindowTitle("Converter - by cms")
        self.setFixedSize(250, 140)

        # self.update_btn = QtWidgets.QPushButton(text='check for update')
        # self.update_btn.clicked.connect(self.check_for_update)

        self.text = QtWidgets.QLabel(self.intro)
        self.text.setAlignment(QtCore.Qt.AlignCenter)

        self.logo = QtWidgets.QLabel(self.waiting_logo_content)
        self.logo.setStyleSheet('font-size: 35px')
        self.logo.setAlignment(QtCore.Qt.AlignCenter)

        self.progress = QtWidgets.QProgressBar(self)
        self.progress.hide()

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.logo)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.progress)
        # self.layout.addWidget(self.update_btn)

        self.setLayout(self.layout)

        self.setAcceptDrops(True)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlag(QtCore.Qt.WindowFullscreenButtonHint, False)

        # self.updater = Updater(parent=self)
        # self.updater.signal.finished.connect(self.handle_download_finished)
        # self.updater.signal.progress_update.connect(
        #     self.handle_progress_update)
        # self.updater.signal.start_download.connect(self.handle_start_download)
        # self.updater.signal.check_for_update.connect(
        #     self.handle_check_for_update)

    # def handle_check_for_update(self, update_object):
    #     print('got\n')
    #     print(update_object)
    #     if update_object['available']:
    #         print('re connect to do_update')
    #         self.update_btn.setText('update')
    #         self.update_btn.clicked.connect(self.do_update)

    # def handle_start_download(self, app_size):
    #     print('got app size: {}'.format(str(app_size)))
    #     self.progress.reset()
    #     self.progress.show()
    #     self.progress.setMaximum(app_size)

    # def handle_progress_update(self, progress):
    #     # print('progress update: {}'.format(str(progress)))
    #     self.progress.setValue(progress)

    # def handle_download_finished(self):
    #     print('download finish')

    # def check_for_update(self):
    #     self.updater.start()

    # def do_update(self):
    #     self.updater.set_action('download')
    #     self.updater.start()

    def file_hover(self):
        self.setStyleSheet("background-color: #414145; color: white")
        self.text.setText('Oh yeah, put down')
        self.logo.setText(self.hover_logo_content)

    def waiting(self):
        self.logo.setText(self.waiting_logo_content)
        self.text.setText(self.intro)

    def running(self, files_count):
        self.setStyleSheet("")
        self.progress.show()
        self.progress.setMaximum(files_count)
        self.progress.setValue(0)
        self.logo.setText(self.running_logo_content)
        self.text.setText("Converting...")

    def show_msg(self, title, text, information, icon=None):
        msg = QtWidgets.QMessageBox(self)
        msg.setWindowTitle(title)
        if icon:
            msg.setIcon(icon)
        msg.setInformativeText(information)
        msg.setText(text)
        msg.exec_()

    @QtCore.Slot()
    def complete(self, result):
        self.show_msg(
            'Success', 'Convertion complete!',
            'All {} file(s), success {} file(s), Overall {} references.\n\nRefMan exported files are in:\n{}\n\n{}'.format(
                result['files_count'], result['suc_count'],
                result['entries_count'], '\n'.join(
                    ['>{}: {}'.format(i+1, p) for i, p in enumerate(result['dump_file_paths'])]),
                '' if len(
                    result['exceptions']) == 0 else 'Noticed that there are some files converted failed, are they EndNote format text files?'
            ),
            # QtWidgets.QMessageBox.Information
        )
        self.waiting()
        self.progress.reset()
        self.progress.hide()

    @QtCore.Slot()
    def update_progress(self):
        self.progress.setValue(self.progress.value() + 1)

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()
            self.file_hover()

    def dragLeaveEvent(self, e):
        self.waiting()

    def dropEvent(self, e):
        files = [url.toLocalFile() for url in e.mimeData().urls()]
        self.waiting()
        self.running(len(files))
        con = Converter(files)
        con.signals.result.connect(self.complete)
        con.signals.finished.connect(self.update_progress)
        con.start()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
