# -*- coding: utf-8 -*-
"""
Created on Wed May 22 18:17:01 2024

@author: ashwe
"""

import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "simple-algo",
    version = "0.0.0",
    author = "ashwe",
    author_email = "",
    description = (""),
    long_description = read('README.md'),
)