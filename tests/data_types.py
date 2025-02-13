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
        ("20190924143134^YYYYMMDDHHMMSS", "2019-09-24T14:31:34", "20190924143134"),
        ("20250204141403.403+0100", "2025-02-04T14:14:03.403000+01:00", "20250204141403.403+0100"),
        ("20250204141403.03", "2025-02-04T14:14:03.030000", "20250204141403.03")
    ]
)
def test_datetime(input_string, isoformat, string_repr):

    delimiters = HL7Delimiters(*"|^~\\&")

    dt = HL7Datetime(input_string, delimiters)
    assert dt.isoformat() == isoformat
    assert str(dt) == string_repr
