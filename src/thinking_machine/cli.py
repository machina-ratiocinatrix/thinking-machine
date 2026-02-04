# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from .machine import machine
import click


@click.command()
# @click.option('--count', default=1, help='number of attempts')
# and use it in the commend as --count=1
# @click.argument('arg')
def run(): #arg):  # (count, arg): if with option.
    click.echo('Running package-name') # with') + arg)
    machine() #arg)
