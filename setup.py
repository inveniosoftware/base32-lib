# -*- coding: utf-8 -*-
#
# This file is part of base32-lib
# Copyright (C) 2019 CERN.
# Copyright (C) 2019 Northwestern University,
#                    Galter Health Sciences Library & Learning Center.

# base32-lib is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Small library to generate, encode and decode random base32 strings."""

import os

from setuptools import setup

readme = open('README.rst').read()
history = open('CHANGES.rst').read()

install_requires = [
    'six>=1.10'
]

tests_require = [
    'check-manifest>=0.25',
    'coverage>=4.0',
    'isort>=4.2.2',
    'pydocstyle>=1.0',
    'pytest-cov>=1.8.0',
    'pytest-pep8>=1.0.6',
    'pytest-runner>=2.7.0',
    'pytest>=3.6.0',
]

extras_require = {
    'docs': [
        'Sphinx>=1.4.2',
    ],
    'tests': tests_require
}


extras_require['all'] = []
for reqs in extras_require.values():
    extras_require['all'].extend(reqs)

setup_requires = [
    'pytest-runner>=2.7.0'
]

# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join('base32_lib', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='base32-lib',
    version=version,
    description=__doc__,
    long_description=readme + '\n\n' + history,
    keywords='base32 identifiers',
    license='MIT License',
    author='Invenio Software',
    author_email='info@inveniosoftware.org',
    url='https://github.com/inveniosoftware/base32-lib',
    packages=[
        'base32_lib',
    ],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
