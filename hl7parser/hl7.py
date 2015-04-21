# -*- encoding: utf-8 -*-
"""
A simple HL7 parser. Construct a new Message object with a HL7 message
and access the contents of the message via object attributes. Segment fields
can be accessed generically via a list or configured to be accesible via named
attributes.

A sample config for the PID-segment is included with this code.

>>> sample_message = \"\"\"\\
... MSH|^~\&|ADT1|GOOD HEALTH HOSPITAL|GHH LAB, INC.|GOOD HEALTH HOSPITAL|\
198808181126|SECURITY|ADT^A01^ADT_A01|MSG00001|P|2.7|
... EVN|A01|200708181123||
... PID|1||PATID1234^5^M11^ADT1^MR^GOOD HEALTH HOSPITAL~123456789^^^USSSA^SS||\
EVERYMAN^ADAM^A^III~Conqueror^Norman^the^II||19610615|M||C|\
2222 HOME STREET^^GREENSBORO^NC^27401-1020|GL|(555) 555-2004|(555)555-2004||\
S|| PATID12345001^2^M10^ADT1^AN^A|444333333|987654^NC|
... NK1|1|NUCLEAR^NELDA^W|SPO^SPOUSE||||NK^NEXT OF KIN
... PV1|1|I|2000^2012^01||||004777^ATTEND^AARON^A|||SUR||||ADM|A0|\"\"\"
>>> message = HL7Message(sample_message)
>>> print message.pid.patient_name
EVERYMAN^ADAM^A^III~Conqueror^Norman^the^II
>>> print message.pid.patient_name[0].family_name
EVERYMAN
>>> print message.pid.patient_name[0].given_name
ADAM
>>> print message.msh.message_type
ADT^A01^ADT_A01
"""

from __future__ import unicode_literals

import hl7parser.hl7_data_types as data_types
from hl7parser.hl7_segments import segment_maps


class HL7Delimiters(object):
    """
        Represents a set of different separators as defined by the HL7 standard
    """
    def __init__(
        self,
        field_separator,
        component_separator,
        rep_separator,
        escape_char,
        subcomponent_separator
    ):
        self.field_separator = field_separator
        self.component_separator = component_separator
        self.rep_separator = rep_separator
        self.escape_char = escape_char
        self.subcomponent_separator = subcomponent_separator

    def __unicode__(self):
        return (self.field_separator + self.component_separator +
                self.rep_separator + self.escape_char +
                self.subcomponent_separator)

    def __str__(self):
        return self.__unicode__()


class HL7Segment(object):
    def __init__(self, segment, delimiters=None):
        if delimiters is None:
            self.delimiters = HL7Delimiters(*"|^~\&")
        else:
            self.delimiters = delimiters

        try:
            segment = segment.decode("utf-8")
        except UnicodeEncodeError:
            pass

        # split into individual fields
        self.fields = segment.split(self.delimiters.field_separator)
        self.fields_length = len(self.fields)

        # the type of the segment is defined in the first field
        self.type = self.fields[0]

        # get the standard definitions for this type
        field_definitions = segment_maps.get(self.type, None)

        # if definitions for this type are found iterate over
        # fields in the input data
        if field_definitions:
            # Pad fields
            self.fields += (
                [''] * (len(field_definitions) + 1 - len(self.fields))
            )
            for index, field_definition in enumerate(field_definitions):
                # get the field name
                field_name = field_definition[0]
                # get the field Type (defaults to HL7DataType)
                DataType = field_definition[1]["type"]
                value = self.fields[index + 1]
                if not field_definition[1]["repeats"]:
                    value = DataType(value, self.delimiters)
                else:
                    value = data_types.HL7RepeatingField(
                        DataType, value, self.delimiters)
                setattr(self, field_name, value)
                self.fields[index + 1] = value
        else:
            # if the segment is unknown create a generic DataObject for each
            # field
            for index, value in enumerate(self.fields[1:]):
                if self.delimiters.rep_separator in value:
                    self.fields[index + 1] = data_types.HL7RepeatingField(
                        data_types.HL7DataType, value, self.delimiters)
                else:
                    self.fields[index + 1] = data_types.HL7DataType(
                        value, self.delimiters)

    def __unicode__(self):
        return self.delimiters.field_separator.join(
            map(unicode, self.fields[0:self.fields_length]))

    def __str__(self):
        return self.__unicode__().encode("utf-8")

    def __getitem__(self, idx):
        """ returns the requested component """
        # shift index one down, since the type field is ignored
        return self.fields[idx + 1]

    def __len__(self):
        return len(self.fields) - 1


class HL7Message(object):
    def __init__(self, message):
        self.message = message
        # list of segments of this message
        # => list of tupels (segment_type, HL7Segment object)
        segments = []
        # dictionary which saves the position of the seqments in the
        # list for fast lookup in __getattr__
        self.segment_position = {}
        self.delimiters = HL7Delimiters(*message[3:8])

        for segment in message.splitlines():
            # create an HLSegment object from the raw data of this segment
            # (i.e. line)
            segment = HL7Segment(segment, self.delimiters)
            # append it to the list of segments
            segment_type = segment.type.lower()
            segments.append((segment_type, segment))

            position = len(segments) - 1

            if segment_type in self.segment_position:
                # if a segment of this type already exists make the postiton
                # entry a list of positions
                if not isinstance(self.segment_position[segment_type], list):
                    self.segment_position[segment_type] = (
                        [self.segment_position[segment_type], position])
                # if it already exists and is a list, just append the new
                # position
                else:
                    self.segment_position[segment_type].append(position)
            # if it doesn't exist just save the position
            else:
                self.segment_position[segment_type] = position

        self.segments = segments

        self.header = self.msh
        self.type = self.header.fields[8]

    def __getattr__(self, attr):
        if attr in self.segment_position:
            positions = self.segment_position[attr]
            if isinstance(positions, list):
                return [self.segments[p][1] for p in positions]
            else:
                return self.segments[positions][1]
        else:
            raise AttributeError(
                "{0!r} object has no attribute {1!r}"
                .format(self.__class__, attr)
            )

    def __unicode__(self):
        return "\n".join([unicode(x[1]) for x in self.segments])

    def __str__(self):
        return self.__unicode__().encode("utf-8")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
