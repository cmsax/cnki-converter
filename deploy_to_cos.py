#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: cnki-converter/deploy_to_cos.py
# Author: MingshiCai i@unoiou.com
# Created Date: 2019-10-11 11:41:51
# ----
# Last Modified:
# Modified By:
# ----
# Copyright (c) 2019 MingshiCai i@unoiou.com
# appid 已在配置中移除,请在参数 Bucket 中带上 appid。Bucket 由 BucketName-APPID 组成
# 1. 设置用户配置, 包括 secretId，secretKey 以及 Region
# -*- coding=utf-8
import sys
import json
import logging
from os import getenv
from platform import system

from qcloud_cos import CosConfig, CosS3Client
from utils import os_type

logging.basicConfig(level=logging.INFO, stream=sys.stdout)


class Uploader():
    """Uploader
    """

    def __init__(self, app_name=None):
        """init

        Args:
            app_name: cos namespace
        """
        assert app_name
        self.app_name = app_name
        self.__os = os_type()

        secret_id = getenv('COS_SECRETID')
        secret_key = getenv('COS_SECRETKEY')
        region = getenv('COS_REGION')
        token = None
        scheme = 'https'
        config = CosConfig(Region=region, SecretId=secret_id,
                           SecretKey=secret_key, Token=token, Scheme=scheme)

        self.__client = CosS3Client(config)
        self.__bucket = getenv('COS_BUCKET')

        self.tag = getenv('TRAVIS_TAG', 'latest')
        logging.info('tag: {}, os: {}'.format(self.tag, self.__os))
        self.dl = ''

    @property
    def __file_name(self):
        return {
            'mac': 'CNKI-Converter-macOS.app.tar',
            'win': 'CNKI-Converter-windows.exe',
            # 'linux': ''
        }[self.__os]

    @property
    def __file_key(self):
        """like `/apps/releases/app_name/win/v1.2.3/app_name.exe`
        """
        return '/apps/releases/{}/{}/{}/{}'.format(
            self.app_name, self.__os, self.tag, self.__file_name
        )

    def __upload(self):
        res = self.__client.upload_file(
            Bucket=self.__bucket, Key=self.__file_key,
            LocalFilePath='./dist/{}'.format(self.__file_name),
            EnableMD5=False)
        self.dl = res['Location']

    def __dump(self):
        logging.info('dl link: {}'.format(self.dl))
        with open('./dist/{}_mirror.json'.format(self.__os), 'w+') as f:
            json.dump({'url': 'https://{}'.format(self.dl)}, f)

    def run(self):
        """Upload binaries to tencent cos against linux, mac and Windows.
        """
        self.__upload()
        self.__dump()
        logging.info('deploy to cos success')


if __name__ == "__main__":
    logging.info('start deploying to tencent cos')
    uploader = Uploader(app_name='cnki-converter')
    uploader.run()
