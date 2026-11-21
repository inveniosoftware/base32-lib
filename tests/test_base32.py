# SPDX-FileCopyrightText: 2019 CERN.
# SPDX-FileCopyrightText: 2019 Northwestern University,
# SPDX-License-Identifier: MIT

"""Provider tests."""

import re

import pytest

from base32_lib import base32


#
# Test encode
#
def test_basic_encode():
    assert base32.encode(32) == "10"
    assert base32.encode(1234) == "16j"


def test_encode_hyphenates():
    assert base32.encode(1234, split_every=1) == "1-6-j"

    with pytest.raises(ValueError):
        assert base32.encode(1234, split_every=-1)


def test_encode_min_length():
    assert base32.encode(1234, min_length=4) == "016j"
    assert base32.encode(1234, min_length=2) == "16j"
    assert base32.encode(1234, min_length=0) == "16j"
    assert base32.encode(1234, min_length=-1) == "16j"


def test_encode_checksum():
    assert base32.encode(1234, checksum=True) == "16j82"


def test_encode_number():
    assert base32.encode(0) == "0"

    with pytest.raises(ValueError):
        base32.encode(-1)


#
# Test generate
#
def test_generate_length():
    assert len(base32.generate(length=2)) == 2

    with pytest.raises(ValueError):
        assert base32.generate(length=-1)


def test_generate_hyphenate():
    identifier = base32.generate(length=3, split_every=1)

    assert len(identifier) == 3 + 2
    assert identifier.count("-") == 2

    with pytest.raises(ValueError):
        assert base32.generate(split_every=-1)

    identifier = base32.generate(length=3, split_every=0)
    assert identifier.count("-") == 0

    identifier = base32.generate(length=3, split_every=3)
    assert identifier.count("-") == 0

    identifier = base32.generate(length=3, split_every=4)
    assert identifier.count("-") == 0


def test_generate_checksum():
    identifier = base32.generate(length=3, checksum=True)

    # checksum is always 2 digits affixed at the end
    assert len(identifier) == 3
    assert re.match(r"\d\d$", identifier[-2:])

    # hyphenation is done after checksum
    identifier = base32.generate(length=3, split_every=1, checksum=True)
    assert len(identifier) == 3 + 2
    assert re.match(r"\d-\d$", identifier[-3:])

    with pytest.raises(ValueError):
        assert base32.generate(length=2, checksum=True)


#
# Test decode
#
def test_basic_decode():
    assert base32.decode("16j") == 1234


def test_decode_normalizes_symbols():
    assert base32.decode("abcdefghijklmnopqrstvwxyz") == base32.decode(
        "ABCDEFGHIJKLMNOPQRSTVWXYZ"
    )
    assert base32.decode("IL1O0ilo") == base32.decode("11100110")
    assert base32.decode("1-6-j") == base32.decode("16j")


def test_decode_raises_for_invalid_string():
    with pytest.raises(ValueError):
        base32.decode("Ü'+?")

    with pytest.raises(ValueError):
        base32.decode("IOU20D011ARS")


def test_decode_0_padded_equivalent_to_non_0_padded():
    assert base32.decode("016j") == base32.decode("16j")


def test_decode_checksum():
    assert base32.decode("16j82", checksum=True) == 1234


def test_decode_invalid_checksum():
    with pytest.raises(ValueError):
        assert base32.decode("16j44", checksum=True)


def test_decode_checksum_with_hyphen_inside_checksum():
    # encode() hyphenates after appending the checksum, so a hyphen can
    # land between (or right before) the two checksum digits.
    assert base32.encode(12345, split_every=4, checksum=True) == "c1s2-0"
    assert base32.decode("c1s2-0", checksum=True) == 12345
    assert base32.decode("1-6-j-8-2", checksum=True) == 1234
    assert base32.decode("16j-82", checksum=True) == 1234


def test_decode_checksum_roundtrip_with_split_every():
    for number in range(0, 5000, 7):
        for split_every in range(0, 6):
            encoded = base32.encode(number, split_every=split_every, checksum=True)
            assert base32.decode(encoded, checksum=True) == number


def test_decode_checksum_rejects_non_digit_checksum():
    with pytest.raises(ValueError):
        base32.decode("16j+8", checksum=True)

    with pytest.raises(ValueError):
        base32.decode("16j٨٢", checksum=True)
