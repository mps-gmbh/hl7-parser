# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from hl7parser.hl7 import HL7Delimiters
from hl7parser.hl7_data_types import HL7Datetime


@pytest.mark.parametrize(
    "input_string, isoformat, string_repr",
    [
        ("198808181126", "1988-08-18T11:26:00", "198808181126"),
        ("", "", ""),
        ("2010", "2010-01-01T00:00:00", "2010"),
        ("-200", "", ""),
        ("20190924143134^YYYYMMDDHHMMSS", "2019-09-24T14:31:34", "20190924143134")
    ]
)
def test_datetime(input_string, isoformat, string_repr):

    delimiters = HL7Delimiters(*"|^~\&")
    dt = HL7Datetime(input_string, delimiters)
    assert dt.isoformat() == isoformat
    assert str(dt) == string_repr
