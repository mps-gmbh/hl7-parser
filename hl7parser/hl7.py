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
>>> print(message.pid.patient_name)
EVERYMAN^ADAM^A^III~Conqueror^Norman^the^II
>>> print(message.pid.patient_name[0].family_name)
EVERYMAN
>>> print(message.pid.patient_name[0].given_name)
ADAM
>>> print(message.msh.message_type)
ADT^A01^ADT_A01
"""

from __future__ import unicode_literals

from __future__ import absolute_import
import re
import sys

import hl7parser.hl7_data_types as data_types
from hl7parser.hl7_segments import segment_maps
from six.moves import map
import six
from six.moves import range

class UnicodeMixin(object):  # pragma: no cover

  """Mixin class to handle defining the proper __str__/__unicode__
  methods in Python 2 or 3."""

  if sys.version_info[0] >= 3: # Python 3
      def __str__(self):
          return self.__unicode__()
  else:  # Python 2
      def __str__(self):
          return self.__unicode__().encode('utf8')

class HL7Delimiters(UnicodeMixin):
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


class HL7Segment(UnicodeMixin):

    def __init__(self, segment, delimiters=None):
        if delimiters is None:
            self.delimiters = HL7Delimiters(*"|^~\&")
        else:
            self.delimiters = delimiters

        if sys.version_info.major == 2:  # pragma: no cover
            try:
                segment = segment.decode("utf-8")
            except UnicodeEncodeError:
                pass

        # split initial content into individual fields
        initial_content = segment.split(self.delimiters.field_separator)

        # the type of the segment is defined in the first field
        self.type = initial_content[0]
        self.fields = []

        # get the standard definitions for this type
        self.field_definitions = segment_maps.get(self.type, [])
        self.named_fields = {}

        # iterate over predefined fields, remember index in `named_fields`
        # and initialize fields
        index_override_found = False
        for index, definition in enumerate(self.field_definitions):
            if definition[1]["index"] is not None:
                definition_index = definition[1]["index"]
                index_override_found = True
            else:
                if index_override_found:
                    raise Exception("Regular cell type after one with index override found")
                definition_index = index
            self.named_fields[definition[0]] = definition_index
            while len(self.fields) != definition_index:
                self.fields.append(data_types.HL7DataType("", self.delimiters))
            self.fields.append(definition[1]["type"]("", self.delimiters))

        # fill fields with initial content
        for index, content in enumerate(initial_content[1:]):
            self[index] = content

    def __unicode__(self):
        """
            Generates the string representation of this message.
            Trailing empty segments will be cut off.
        """
        field_separator = self.delimiters.field_separator
        result = field_separator.join(map(six.text_type, [self.type] + self.fields))
        result = re.sub(
            "{0}+$".format(re.escape(field_separator)),
            field_separator,
            result
        )
        return result

    def __getitem__(self, idx):
        """ returns the requested component """
        return self.fields[idx]

    def __getattr__(self, attr):
        try:
            return self[self.named_fields[attr]]
        except (KeyError, IndexError):
            raise AttributeError(attr)

    def require_length(self, length):
        """
            Makes sure the segment has at least length "length".
            If "length" is greater than the current length, new empty fields are added.

            :param length:
                The required length
            :type length:
                int
        """
        if length < len(self):
            return
        for _ in range(length - len(self)):
            self.fields.append(data_types.HL7DataType("", self.delimiters))

    def __setitem__(self, attr, value):
        if isinstance(attr, int):
            self.require_length(attr + 1)

            try:
                field_definition = self.field_definitions[attr][1]
            except IndexError:
                data_type = data_types.HL7DataType
                repeats = self.delimiters.rep_separator in value
            else:
                data_type = field_definition["type"]
                repeats = field_definition["repeats"]

            if not repeats:
                self.fields[attr] = data_type(value, self.delimiters)
            else:
                self.fields[attr] = data_types.HL7RepeatingField(
                    data_type, value, self.delimiters
                )
        else:
            raise TypeError("Segment indexes must be integers.")

    def __len__(self):
        return len(self.fields)


class HL7Message(UnicodeMixin):
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

    def __unicode__(self):  # pragma: no cover
        return "\n".join([six.text_type(x[1]) for x in self.segments])
