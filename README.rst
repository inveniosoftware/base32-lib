..
   This file is part of base32-lib
   Copyright (C) 2019 CERN.
   Copyright (C) 2019 Northwestern University,
                      Galter Health Sciences Library & Learning Center.

   base32-lib is free software; you can redistribute it and/or modify it
   under the terms of the MIT License; see LICENSE file for more details.


=================
base32-lib
=================

.. image:: https://img.shields.io/travis/inveniosoftware/base32-lib.svg
        :target: https://travis-ci.org/inveniosoftware/base32-lib

.. image:: https://img.shields.io/coveralls/inveniosoftware/base32-lib.svg
        :target: https://coveralls.io/r/inveniosoftware/base32-lib

.. image:: https://img.shields.io/github/tag/inveniosoftware/base32-lib.svg
        :target: https://github.com/inveniosoftware/base32-lib/releases

.. image:: https://img.shields.io/pypi/dm/base32-lib.svg
        :target: https://pypi.python.org/pypi/base32-lib

.. image:: https://img.shields.io/github/license/inveniosoftware/base32-lib.svg
        :target: https://github.com/inveniosoftware/base32-lib/blob/master/LICENSE


Small library to generate, encode and decode random base32 strings with nice
properties.

Usage
=====

.. code-block:: python

    import base32_lib as base32

    # Generate
    ## Generate a random identifier
    base32.generate()
    # -> 'abcd1234'

    # Generate a random identifier with bells and whistle
    base32.generate(length=10, split_every=5, checksum=True)
    # -> '3sbk2-5j060'

    # Encode a pre-existing number
    base32.encode(1234, split_every=3, checksum=True) == "16j-82"

    # Decode an identifier
    base32.decode("16j-82", checksum=True) == 1234

    base32.decode("16i-82", checksum=True)
    # raises ValueError

Features
========

- Generation, encoding and decoding of base32 strings
- Douglas Crockford base32 encoding
- URL-safe strings with no problematic special characters
- Decoding of any-case strings
- Configurable length strings
- Randomness through cryptographically secure random number generator
- Optional ISO-7064 checksum
- Optional hyphenation


Installation
============

The base32-lib package is on PyPI so all you need is:

.. code-block:: console

    pip install base32-lib


Development
===========

.. code-block:: console

    pipenv run pip install -e .[docs,tests]

Tests
-----

.. code-block:: console

    pipenv run ./run-tests.sh
