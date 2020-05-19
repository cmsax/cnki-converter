import logging
import uvicorn
from fastapi import FastAPI

from yigesamo import __version__
from yigesamo.converter import converter


app = FastAPI(
    title='CNKI Converter',
    description='A service to convert CNKI ref to RefMan ref records.',
    version=__version__
)

LOGGER = logging.getLogger(__name__)


@app.get('/version')
async def version():
    return __version__


def start_server():
    LOGGER.info('starting server...')
    uvicorn.run(app, host='127.0.0.1', port=5000, log_level='info')


def main():
    start_server()
