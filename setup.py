#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

def readme():
    with open('README.md') as readme_file:
        return readme_file.read()

setup(
    name = 'freediving_analysis',
    version = '1.0.1',
    description = 'freediving_analysis',
    long_description=readme(),
    download_url = 'https://github.com/dellielo/DeepFreedivingAnalysis',
    url = 'https://github.com/dellielo/DeepFreedivingAnalysis',
    author = 'Elodie Dellier',
    author_email = 'dellier.elodie@gmail.com',
    packages = ['freediving_analysis'],
    license = "MIT",
    install_requires = [],
    classifiers = [
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.4',
        ],
    entry_points='''
        [console_scripts]
        
    ''',
    )