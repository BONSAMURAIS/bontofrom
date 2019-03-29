import pytest
from unittest import mock
import bontofrom.convert_exiobase as bex


def test_isdiagonal():
    diag_cell = mock.Mock()
    diag_cell.c = 42
    diag_cell.r = 41
    assert bex.isdiagonal(diag_cell)

    diag_cell.c = 41
    assert not bex.isdiagonal(diag_cell)


def test_isunitneedsconversion():
    assert bex.isunitneedsconversion("TJ")
    assert bex.isunitneedsconversion("Meuro")
    assert bex.isunitneedsconversion("tonnes")
    assert not bex.isunitneedsconversion("kg")

