# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from data_types import (HL7DataType,
                        HL7Datetime,
                        HL7_ExtendedCompositeId,
                        HL7_ExtendedPersonName,
                        HL7_ExtendedTelecommunicationNumber)

def segment_field_options(name, options=None):
    default_options = {
        'required': False,
        'repeats': False,
        'type': HL7DataType
    }
    if options is None:
        options = {}

    default_options.update(options)
    return (name, default_options)


segment_maps = {
    'MSH': [
        segment_field_options('encoding_characters',
                              options = {"required": True}),
        segment_field_options('sending_application'),
        segment_field_options('sending_facility'),
        segment_field_options('receiving_application'),
        segment_field_options('receiving_facility'),
        segment_field_options('message_datetime',
                              options = {"repeats": True, "type": HL7Datetime}),
        segment_field_options('security'),
        segment_field_options('message_type', options = {"required": True}),
        segment_field_options('message_control_id', options = {"required": True}),
        segment_field_options('processing_id', options = {"required": True}),
        segment_field_options('version_id', options = {"required": True}),
        segment_field_options('sequence_number'),
        segment_field_options('accept_acknowledgment_type'),
        segment_field_options('application_acknowledgment_type'),
        segment_field_options('country_code'),
        segment_field_options('character_set', options = {"repeats": True}),
        segment_field_options('principal_language_of_message'),
        segment_field_options('alternate_character_set_handling_scheme'),
        segment_field_options('message_profile_identifier', options = {"repeats": True}),
        segment_field_options('sending_responsible_organization'),
        segment_field_options('receiving_responsible_organization'),
        segment_field_options('sending_network_address'),
        segment_field_options('receiving_network_address'),
    ],
    'EVN': [
        segment_field_options('event_type_code'),
        segment_field_options('recorded_datetime', options = { "required": True}),
        segment_field_options('datetime_planned_event'), 
        segment_field_options('event_reason_code'),
        segment_field_options('operator_id', options = {"repeats": True}),
        segment_field_options('event_occured'),
        segment_field_options('event_facility'),
    ],
    'PID': [
        # (field name, repeats)
        segment_field_options('set_id_pid'),
        segment_field_options('patient_id'),
        segment_field_options('patient_identifier_list',
                              options = {"required": True, "repeats": True, "type": HL7_ExtendedCompositeId}),
        segment_field_options('alternate_patient_id_pid'),
        segment_field_options('patient_name',
                              options = {"required": True, "repeats": True, "type": HL7_ExtendedPersonName}),
        segment_field_options('mothers_maiden_name',
                              options = {"repeats": True, "type": HL7_ExtendedPersonName}),
        segment_field_options('datetime_of_birth', options = {"type": HL7Datetime}),
        segment_field_options('administrative_sex'),
        segment_field_options('patient_alias'),
        segment_field_options('race', options = {"required": True}),
        segment_field_options('patient_address', options = {"required": True}),
        segment_field_options('county_code'),
        segment_field_options('phone_number_home',
                              options = {"required": True, "type": HL7_ExtendedTelecommunicationNumber}),
        segment_field_options('phone_number_business',
                              options = {"required": True, "type": HL7_ExtendedTelecommunicationNumber}),
        segment_field_options('primary_language'),
        segment_field_options('marital_status'),
        segment_field_options('religion'),
        segment_field_options('patient_account_number'),
        segment_field_options('ssn_number_patient'),
        segment_field_options('drivers_license_number_patient'),
        segment_field_options('mothers_identifier', options = {"repeats": True}),
        segment_field_options('ethnic_group', options = {"required": True}),
        segment_field_options('birth_place'),
        segment_field_options('multiple_birth_indicator'),
        segment_field_options('birth_order'),
        segment_field_options('citizenship', options = {"required": True}),
        segment_field_options('veterans_military_status'),
        segment_field_options('nationality'), 
        segment_field_options('patient_death_date_and_time'),
        segment_field_options('patient_death_indicator'),
        segment_field_options('identity_unknown_indicator'),
        segment_field_options('identity_reliability_code', options = {"required": True}),
        segment_field_options('last_update_datetime'),
        segment_field_options('last_update_facility'),
        segment_field_options('species_code'),
        segment_field_options('breed_code'),
        segment_field_options('strain'),
        segment_field_options('production_class_code', options = {"repeats": True}),
        segment_field_options('tribal_citizenship', options = {"repeats": True}),
        segment_field_options('patient_telecommunication_information', options = {"repeats": True})
    ],
}
