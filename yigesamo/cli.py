#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: cnki-converter/cli.py
# Author: MingshiCai i@unoiou.com
# Date: 2020-04-16 15:44:50
import click

from converter import converter


@click.command('run')
@click.option('-f', '--file', help='cnki reference file location, *.txt')
def run(file):
    fp, count = converter(file)
    print((
        'Done! Converted {} items, '
        'output file is located in:\n{}\n'
    ).format(count, fp))


if __name__ == "__main__":
    run()
