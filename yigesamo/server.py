#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: yigesamo\server.py
# Author: MingshiCai i@unoiou.com
# Date: 2020-05-19 20:55:47
import arrow
import logging
import os
import time
import uvicorn

from fastapi import (
    BackgroundTasks, FastAPI, File, UploadFile, Response, HTTPException
)
from fastapi.responses import FileResponse, RedirectResponse
from uuid import uuid4

from yigesamo import __version__
from yigesamo.constant import HTML
from yigesamo.converter import converter


app = FastAPI(
    title='CNKI Converter',
    description='A service to convert CNKI ref to RefMan ref records.',
    version=__version__
)

LOGGER = logging.getLogger(__name__)
TEMP_FILE_DIR = 'temp'


class Helper:
    @staticmethod
    def get_random_file_name():
        return '{}_{}.txt'.format(
            uuid4().hex, arrow.get().format('YYYY-MM-DD')
        )

    @staticmethod
    def get_path(file_name):
        return os.path.join(TEMP_FILE_DIR, file_name)

    @classmethod
    def remove_temp_file(cls, q):
        """Remove user content.
        """
        path = cls.get_path(file_name=q)
        # sleep 30s to let user download file
        time.sleep(30)
        if os.path.exists(path):
            os.remove(path)
            LOGGER.info('file {} removed'.format(path))
        else:
            LOGGER.info('file {} not exists'.format(path))

    @classmethod
    def make_file_response(cls, text_content):
        """Redirect to file download page.
        """
        file_name = cls.get_random_file_name()
        path = cls.get_path(file_name)
        LOGGER.info('path: {}'.format(path))

        with open(path, 'wb') as f:
            f.write(text_content)

        # here convert user post text
        try:
            converter(path, True)
        except Exception as e:
            raise HTTPException(418, "I'm a teapot.")

        return RedirectResponse(
            '/result?q={}'.format(file_name),
            status_code=307
        )

    @classmethod
    def get_file_response(cls, q):
        path = cls.get_path(file_name=q)
        if not os.path.exists(path):
            raise HTTPException(404, 'file not found')

        return FileResponse(
            path=path,
            media_type='application/octet-stream',
            filename='convert_result_{}.ris'.format(q.split('_')[0])
        )


@app.get('/converter')
def web_app():
    return Response(
        content=HTML.replace('VERSION', __version__),
        media_type='text/html; charset=utf-8'
    )


@app.post('/converter')
async def convert_upload_file(file: UploadFile = File(...)):
    file_content = await file.read()
    return Helper.make_file_response(file_content)


@app.post('/result')
@app.get('/result')
async def get_result(q, background_tasks: BackgroundTasks):
    background_tasks.add_task(Helper.remove_temp_file, q)
    return Helper.get_file_response(q)


@app.get('/')
async def health():
    return RedirectResponse('/converter')


def start_server():
    if not os.path.exists(TEMP_FILE_DIR):
        os.mkdir(TEMP_FILE_DIR)

    LOGGER.info('starting server...')
    uvicorn.run(app, host='0.0.0.0', port=5000, log_level='info')


def main():
    start_server()
