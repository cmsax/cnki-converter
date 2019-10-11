
# -*- coding: utf-8 -*-
# File: cnki-converter/update.py
# Author: MingshiCai i@unoiou.com
# Created Date: 2019-10-10 19:53:29
# ----
# Last Modified:
# Modified By:
# ----
# Copyright (c) 2019 MingshiCai i@unoiou.com
from platform import system

from PySide2 import QtCore, QtWidgets
from requests import get


class UpdaterSignals(QtCore.QObject):
    finished = QtCore.Signal()
    check_for_update = QtCore.Signal(object)
    progress_update = QtCore.Signal(object)
    start_download = QtCore.Signal(int)


class Updater(QtCore.QRunnable):
    def __init__(self, action='check'):
        super(Updater, self).__init__()
        self.current_version = 'v1.4.0'
        self.latest_version = None
        self.download_url = None
        self.signal = UpdaterSignals()
        self.action = action
        self.setAutoDelete(False)

    @property
    def os(self):
        name = system().lower()
        if name == 'darwin':
            return 'mac'
        elif name == 'linux':
            return 'linux'
        return 'windows'

    @property
    def update_available(self):
        return self.download_url and (
            self.current_version != self.latest_version)

    @property
    def api(self):
        return 'https://api.unoiou.com/apps/version?app_name=cnki-converter&os={}'.format(self.os)

    def set_action(self, action):
        self.action = action

    def check(self):
        print('start checking for updates')
        res = get(self.api)
        data = res.json()['data']
        self.latest_version = data.get('version')
        self.download_url = data.get('url')
        print(data)
        self.signal.check_for_update.emit({
            'available': self.update_available, 'version': self.latest_version,
            'download_url': self.download_url
        })

    def download(self):
        print('start downloading binary')
        res = get(self.download_url, stream=True)
        print(res)
        length = res.headers.get('content-length')
        if not length:
            self.signal.finished.emit()
            return 1
        print("got length")
        self.signal.start_download.emit(length)
        dl = 0
        with open('./cnki-converter-new.tar', 'wb+') as f:
            for chunk in res.iter_content(chunk_size=2048):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    dl += len(chunk)
                    self.signal.progress_update.emit(dl)
            self.signal.finished.emit()

    def run(self):
        {'check': self.check, 'download': self.download}[self.action]()

    def start(self):
        print('start updater thread')
        QtCore.QThreadPool.globalInstance().start(self)
