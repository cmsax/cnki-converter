FROM python:3.8-slim-buster

LABEL author="Mingshi Cai"
LABEL email="i@unoiou.com"

COPY ./ ./

RUN pip install poetry -i https://pypi.tuna.tsinghua.edu.cn/simple some-package
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

CMD ["serve"]
