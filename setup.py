# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  mixiu-pytest-helper
# FileName:     setup.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/07/31
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from setuptools import setup, find_packages

setup(
    name='mixiu-pytest-helper',
    version='0.0.3',
    description='This is my mixiu pytest helper package',
    long_description='This is my mixiu pytest helper package',
    author='ckf10000',
    author_email='ckf10000@sina.com',
    url='https://github.com/ckf10000/mixiu-pytest-helper',
    packages=find_packages(),
    install_requires=[
        'pytest>=8.3.1',
        'mixiu-app-helper>=0.1.2',
        'distributed-logging>=0.0.3',
        'python-apollo-proxy>=0.1.7',
        'middleware-help-python>=0.1.3'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
