#!/bin/env python

from collections import defaultdict

import data_types

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

segment_maps = {
    'MSH': [
        'encoding_characters',
        'sending_application',
        'sending_facility',
        'receiving_application',
        'receiving_facility',
        'message_datetime',
        'security',
        'message_type',
        'message_control_id',
        'processing_id',
        'version_id',
        'sequence_number',
        'accept_acknowledgment_type',
        'application_acknowledgment_type',
        'country_code',
        'character_set',
        'principal_language_of_message',
        'alternate_character_set_handling_scheme',
        'message_profile_identifier',
        'sending_responsible_organization',
        'receiving_responsible_organization',
        'sending_network_address',
        'receiving_network_address',
    ],
    'EVN': [
        'event_type_code',
        'recorded_datetime',
        'datetime_planned_event',
        'event_reason_code',
        'operator_id',
        'event_occured',
        'event_facility',
    ],
    'PID': [
        'set_id_pid',
        'patient_id',
        'patient_identifier_list',
        'alternate_patient_id_pid',
        'patien_name',
        'mothers_maiden_name',
        'datetime_of_birth',
        'administrative_sex',
        'patient_alias',
        'race',
        'patient_address',
        'county_code',
        'phone_number_home',
        'phone_number_business',
        'primary_language',
        'marital_status',
        'religion',
        'patient_account_number',
        'ssn_number_patient',
        'drivers_license_number_patient',
        'mothers_identifier',
        'ethnic_group',
        'birth_place',
        'multiple_birth_indicator',
        'birth_order',
        'citizenship',
        'veterans_military_status',
        'nationality',
        'patient_death_date_and_time',
        'patient_death_indicator',
        'identity_unknown_indicator',
        'identity_reliability_code',
        'last_update_datetime',
        'last_update_facility',
        'species_code',
        'breed_code',
        'strain',
        'production_class_code',
        'tribal_citizenship',
        'patient_telecommunication_information',
    ],
}

field_types = {
    'PID' : [
        ('name', data_types.XPN),
        ('mothers_maiden_name', data_types.XPN),
    ]
}

required_segments = [key for (key, value) in segment_types.iteritems() if not value['optional']]
repeating_segments = [key for (key, value) in segment_types.iteritems() if value['repeats']]

class HL7Delimiters(object):
    def __init__(self, composite, subcomposite, field, escape, subsub_composite):
        (self.composite,
         self.subcomposite,
         self.field,
         self.escape,
         self.subsub_composite) = (composite,
                                   subcomposite,
                                   field,
                                   escape,
                                   subsub_composite)


class HL7Segment(object):
    def __init__(self, segment, delimiters=None):
        if delimiters == None:
            self.delimiters = HL7Delimiters(*"|^~\&")
        else:
            self.delimiters = delimiters

        self.composites = segment.split(self.delimiters.composite)
        self.type = self.composites[0]

        fields = dict(field_types.get(self.type, {}))

        composites_map = segment_maps.get(self.type)

        if composites_map:
            for index, value in enumerate(self.composites[1:]):
                field_name = composites_map[index]
                DateType = fields.get(field_name, data_types.HL7DataType)
                setattr(self, composites_map[index], DateType(value, delimiters))

    def __unicode__(self):
        return self.delimiters.composite.join(self.composites)

    def __str__(self):
        return self.__unicode__()




class HL7Message(object):
    def __init__(self, message):
        self.message = message
        segments = defaultdict(list)
        delimiters = HL7Delimiters(*message[3:8])

        for segment in message.splitlines():
            segment = HL7Segment(segment, delimiters)
            if segment_types[segment.type]['repeats']:
                try:
                    segments[segment.type.lower()].append(segment)
                except KeyError:
                    segments[segment.type.lower()] = segment
            else:
                segments[segment.type.lower()] = segment

        self.segments = segments

        self.header = self.msh
        self.type = self.header.composites[8]



    def __getattr__(self, attr):
        try:
            return self.segments[attr]
        except KeyError:
            return getattr(self, attr)


message = HL7Message(sample_message)

print message.pid.name
print message.msh.message_type
