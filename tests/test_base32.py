# -*- coding: utf-8 -*-
#
# This file is part of base32-lib
# Copyright (C) 2019 CERN.
# Copyright (C) 2019 Northwestern University,
#                    Galter Health Sciences Library & Learning Center.

# base32-lib is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Provider tests."""

import re

import pytest

from base32_lib import base32


class TestEncode(object):
    """Encode tests."""

    def test_basic_encode(self):
        assert base32.encode(32) == "10"
        assert base32.encode(1234) == "16j"

    def test_encode_hyphenates(self):
        assert base32.encode(1234, split_every=1) == "1-6-j"

        with pytest.raises(ValueError):
            assert base32.encode(1234, split_every=-1)

    def test_encode_min_length(self):
        assert base32.encode(1234, min_length=4) == "016j"
        assert base32.encode(1234, min_length=2) == "16j"
        assert base32.encode(1234, min_length=0) == "16j"
        assert base32.encode(1234, min_length=-1) == "16j"

    def test_encode_checksum(self):
        assert base32.encode(1234, checksum=True) == "16j82"

    def test_encode_number(self):
        assert base32.encode(0) == "0"

        with pytest.raises(ValueError):
            base32.encode(-1)


class TestGenerate(object):
    """Generate tests."""

    def test_generate_length(self):
        assert len(base32.generate(length=2)) == 2

        with pytest.raises(ValueError):
            assert base32.generate(length=-1)

    def test_generate_hyphenate(self):
        identifier = base32.generate(length=3, split_every=1)

        assert len(identifier) == 3 + 2
        assert identifier.count('-') == 2

        with pytest.raises(ValueError):
            assert base32.generate(split_every=-1)

        identifier = base32.generate(length=3, split_every=0)
        assert identifier.count('-') == 0

        identifier = base32.generate(length=3, split_every=3)
        assert identifier.count('-') == 0

        identifier = base32.generate(length=3, split_every=4)
        assert identifier.count('-') == 0

    def test_generate_checksum(self):
        identifier = base32.generate(length=3, checksum=True)

        # checksum is always 2 digits affixed at the end
        assert len(identifier) == 3
        assert re.match(r'\d\d$', identifier[-2:])

        # hyphenation is done after checksum
        identifier = base32.generate(length=3, split_every=1, checksum=True)
        assert len(identifier) == 3 + 2
        assert re.match(r'\d-\d$', identifier[-3:])

        with pytest.raises(ValueError):
            assert base32.generate(length=2, checksum=True)


class TestDecode(object):
    """Decode tests."""

    def test_basic_decode(self):
        assert base32.decode("16j") == 1234

    def test_decode_normalizes_symbols(self):
        assert (
            base32.decode("abcdefghijklmnopqrstvwxyz") ==
            base32.decode("ABCDEFGHIJKLMNOPQRSTVWXYZ")
        )
        assert base32.decode('IL1O0ilo') == base32.decode('11100110')
        assert base32.decode('1-6-j') == base32.decode('16j')

    def test_decode_raises_for_invalid_string(self):
        with pytest.raises(ValueError):
            base32.decode("Ü'+?")

        with pytest.raises(ValueError):
            base32.decode("IOU20D011ARS")

    def test_decode_0_padded_equivalent_to_non_0_padded(self):
        assert base32.decode('016j') == base32.decode('16j')

    def test_decode_checksum(self):
        assert base32.decode("16j82", checksum=True) == 1234

    def test_decode_invalid_checksum(self):
        with pytest.raises(ValueError):
            assert base32.decode("16j44", checksum=True)
