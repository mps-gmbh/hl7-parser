# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import data_types

from hl7_definitions import segment_maps

sample_message = """\
MSH|^~\&|ADT1|GOOD HEALTH HOSPITAL|GHH LAB, INC.|GOOD HEALTH HOSPITAL|198808181126|SECURITY|ADT^A01^ADT_A01|MSG00001|P|2.7|
EVN|A01|200708181123||
PID|1||PATID1234^5^M11^ADT1^MR^GOOD HEALTH HOSPITAL~123456789^^^USSSA^SS||EVERYMAN^ADAM^A^III||19610615|M||C|2222 HOME STREET^^GREENSBORO^NC^27401-1020|GL|(555) 555-2004|(555)555-2004||S|| PATID12345001^2^M10^ADT1^AN^A|444333333|987654^NC|
NK1|1|NUCLEAR^NELDA^W|SPO^SPOUSE||||NK^NEXT OF KIN
PV1|1|I|2000^2012^01||||004777^ATTEND^AARON^A|||SUR||||ADM|A0|
"""


message_types = {
    'ADT^A04': "Register a patient",
    'ADT^A08': "Update patient information",
    'ADT^A01': "Admit/visit notification",
}

segment_types = {
    'MSH': {'optional': False, 'repeats': False, },
    'EVN': {'optional': False, 'repeats': False, },
    'PID': {'optional': False, 'repeats': False, },
    'NK1': {'optional': True, 'repeats': True, },
    'PV1': {'optional': False, 'repeats': False, },
}


required_segments = [key for (key, value) in segment_types.iteritems() if not value['optional']]
repeating_segments = [key for (key, value) in segment_types.iteritems() if value['repeats']]

class HL7Delimiters(object):
    """
        Represents a set of different separators as defined by the HL7 standard
    """
    def __init__(self, field_separator, component_separator,
                 rep_separator, escape_char, subcomponent_separator):
        (self.field_separator,
         self.component_separator,
         self.rep_separator,
         self.escape_char,
         self.subcomponent_separator) = (field_separator,
                                   component_separator,
                                   rep_separator,
                                   escape_char,
                                   subcomponent_separator)
                                   
    def __unicode__(self):
        return (self.field_separator + self.component_separator + self.rep_separator + self.escape_char +
                self.subcomponent_separator)

    def __str__(self):
        return self.__unicode__()

class HL7Segment(object):
    def __init__(self, segment, delimiters=None):
        if delimiters == None:
            self.delimiters = HL7Delimiters(*"|^~\&")
        else:
            self.delimiters = delimiters

        # split into individual fields
        self.fields = segment.split(self.delimiters.field_separator)
        # the type of the segment is defined in the first field
        self.type = self.fields[0]

        # get the standard definitions for this type
        field_definitions = segment_maps.get(self.type, None)

        # if definitions for this type are found iterate over
        # fields in the input data
        if field_definitions:
            for index, value in enumerate(self.fields[1:]):
                # get the field name
                field_name = field_definitions[index][0]
                # get the field Type (defaults to HL7DataType)
                DataType = field_definitions[index][1]["type"]
                if not field_definitions[index][1]["repeats"]:
                    value = DataType(value, delimiters)
                else:
                    value = data_types.HL7RepeatingField(DataType, value, delimiters)
                setattr(self, field_name, value)
                self.fields[index + 1] = value

    def __unicode__(self):
        return self.delimiters.field_separator.join(map(unicode, self.composites))

    def __str__(self):
        return self.__unicode__()




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
                if not isinstance(list, self.segment_position[segment_type]):
                    self.segment_position[segment_type] = (
                        [self.segment_position[segment_type], position] )
                # if it already exists and is a list, just append the new position
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
            return self.segments[self.segment_position[attr]][1]
        else:
            return getattr(self, attr)


    def __unicode__(self):
        return "\n".join([unicode(x[1]) for x in self.segments])

    def __string__(self):
        return self.__unicode__()

message = HL7Message(sample_message)

#~ print message.pid.name
#~ print message.msh.message_type
