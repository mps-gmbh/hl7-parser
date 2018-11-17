# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import pytest
import mock

from hl7parser.hl7 import HL7Segment
from hl7parser.hl7_data_types import HL7DataType, HL7Datetime, make_cell_type


def test_hl7_segment_require_length():
    segment = HL7Segment("ABC|1|2")

    assert len(segment) == 2

    # requiring less fields than already present should do nothing
    segment.require_length(2)
    assert len(segment) == 2

    segment.require_length(10)
    assert len(segment) == 10


def test_hl7_segment_field_assignment_generic():
    segment = HL7Segment("")

    segment[3] = "ABC"

    assert isinstance(segment.fields[3], HL7DataType)
    assert str(segment) == "||||ABC"


def test_hl7_segment_field_assignment_predefined():
    segment = HL7Segment("EVN|123|20000101|")

    segment[2] = "20010101"

    assert isinstance(segment.fields[2], HL7Datetime)


def test_hl7_segment_field_assignment_error():
    segment = HL7Segment("")

    with pytest.raises(TypeError):
        segment["Hello"] = "ABC"

    with pytest.raises(AttributeError):
        segment.something


def test_invalid_segment_definition():
    """ cell types with "index" definition must come at the end """

    segment_maps = {
        "foo": [
            make_cell_type('foo'),
            make_cell_type('bar', index=3),
            make_cell_type('baz'),
        ]
    }

    with mock.patch("hl7parser.hl7.segment_maps", segment_maps):
        with pytest.raises(Exception):
            HL7Segment("foo|1|2|3")
