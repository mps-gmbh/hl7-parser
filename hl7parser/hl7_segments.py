# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from hl7parser.hl7_data_types import (
    HL7Datetime,
    HL7_MessageType,
    HL7_ExtendedCompositeId,
    HL7_ExtendedPersonName,
    HL7_ExtendedAddress,
    HL7_CodedWithException,
    HL7_ProcessingType,
    HL7_VersionIdentifier,
    HL7_PersonLocation,
)

from hl7parser import hl7_data_types

from hl7parser.hl7_data_types import make_cell_type

segment_maps = {
    'MSH': [
        make_cell_type(
            'encoding_characters',
            options={"required": True}),
        make_cell_type('sending_application'),
        make_cell_type('sending_facility'),
        make_cell_type('receiving_application'),
        make_cell_type('receiving_facility'),
        make_cell_type(
            'message_datetime',
            options={"repeats": True, "type": HL7Datetime}
        ),
        make_cell_type('security'),
        make_cell_type(
            'message_type',
            options={"required": True, "type": HL7_MessageType}
        ),
        make_cell_type('message_control_id', options={"required": True}),
        make_cell_type(
            'processing_id',
            options={"required": True, "type": HL7_ProcessingType}
        ),
        make_cell_type(
            'version_id',
            options={"required": True, "type": HL7_VersionIdentifier}
        ),
        make_cell_type('sequence_number'),
        make_cell_type('accept_acknowledgment_type'),
        make_cell_type('application_acknowledgment_type'),
        make_cell_type('country_code'),
        make_cell_type(
            'character_set',
            options={"repeats": True}
        ),
        make_cell_type(
            'principal_language_of_message',
            options={"type": HL7_CodedWithException}
        ),
        make_cell_type('alternate_character_set_handling_scheme'),
        make_cell_type(
            'message_profile_identifier',
            options={"repeats": True}
        ),
        make_cell_type('sending_responsible_organization'),
        make_cell_type('receiving_responsible_organization'),
        make_cell_type('sending_network_address'),
        make_cell_type('receiving_network_address'),
    ],
    "MSA": [
        make_cell_type('acknowledgement_code'),
        make_cell_type('message_control_id'),
        make_cell_type('text_message'),
    ],
    'EVN': [
        make_cell_type('event_type_code'),
        make_cell_type(
            'recorded_datetime',
            options={"required": True, "type": HL7Datetime}
        ),
        make_cell_type(
            'datetime_planned_event',
            options={"type": HL7Datetime}
        ),
        make_cell_type(
            'event_reason_code',
            options={"type": HL7_CodedWithException}
        ),
        make_cell_type('operator_id', options={"repeats": True}),
        make_cell_type('event_occured'),
        make_cell_type('event_facility'),
    ],
    'PID': [
        # (field name, repeats)
        make_cell_type('set_id_pid'),
        make_cell_type('patient_id'),
        make_cell_type(
            'patient_identifier_list',
            options={
                "required": True,
                "repeats": True,
                "type": HL7_ExtendedCompositeId
            }
        ),
        make_cell_type('alternate_patient_id_pid'),
        make_cell_type(
            'patient_name',
            options={
                "required": True,
                "repeats": True,
                "type": HL7_ExtendedPersonName
            }
        ),
        make_cell_type(
            'mothers_maiden_name',
            options={
                "repeats": True,
                "type": HL7_ExtendedPersonName
            }
        ),
        make_cell_type('datetime_of_birth', options={"type": HL7Datetime}),
        make_cell_type('administrative_sex'),
        make_cell_type('patient_alias'),
        make_cell_type(
            'race',
            options={
                "repeats": True,
                "type": HL7_CodedWithException
            }
        ),
        make_cell_type(
            'patient_address',
            options={
                "required": True,
                "repeats": True,
                "type": HL7_ExtendedAddress,
            }
        ),
        make_cell_type('county_code'),
        make_cell_type('phone_number_home', options={"repeats": True}),
        make_cell_type('phone_number_business', options={"repeats": True}),
        make_cell_type('primary_language'),
        make_cell_type('marital_status'),
        make_cell_type('religion'),
        make_cell_type('patient_account_number'),
        make_cell_type('ssn_number_patient'),
        make_cell_type('drivers_license_number_patient'),
        make_cell_type('mothers_identifier', options={"repeats": True}),
        make_cell_type('ethnic_group', options={"repeats": True}),
        make_cell_type('birth_place'),
        make_cell_type('multiple_birth_indicator'),
        make_cell_type('birth_order'),
        make_cell_type('citizenship', options={"repeats": True}),
        make_cell_type('veterans_military_status'),
        make_cell_type('nationality'),
        make_cell_type('patient_death_date_and_time'),
        make_cell_type('patient_death_indicator'),
        make_cell_type('identity_unknown_indicator'),
        make_cell_type('identity_reliability_code', options={"repeats": True}),
        make_cell_type('last_update_datetime'),
        make_cell_type('last_update_facility'),
        make_cell_type('species_code'),
        make_cell_type('breed_code'),
        make_cell_type('strain'),
        make_cell_type('production_class_code', options={"repeats": True}),
        make_cell_type('tribal_citizenship', options={"repeats": True}),
        make_cell_type(
            'patient_telecommunication_information',
            options={"repeats": True}
        )
    ],
    "MRG": [
        make_cell_type(
            'prior_patient_identifier_list',
            options={
                "required": True,
                "repeats": True,
                "type": HL7_ExtendedCompositeId
            }
        ),
        make_cell_type('prior_alternate_patient_id'),
        make_cell_type('prior_patient_account_number'),
        make_cell_type('prior_patient_id'),
        make_cell_type('prior_visit_number'),
        make_cell_type('prior_alternate_visit_id'),
        make_cell_type(
            'prior_patient_name',
            options={
                "repeats": True,
                "type": HL7_ExtendedPersonName
            }
        ),
    ],
    "PV1": [
        make_cell_type("set_id"),
        make_cell_type(
            "patient_class",
            options={
                "required": True,
                "type": HL7_CodedWithException,
            }
        ),
        make_cell_type("assigned_patient_location", options={"type": HL7_PersonLocation}),
        make_cell_type("admission_type", options={"type": HL7_CodedWithException}),
        make_cell_type("preadmit_number", options={"type": HL7_ExtendedCompositeId}),
        make_cell_type("prior_patient_location", options={"type": HL7_PersonLocation}),
        make_cell_type(
            "attending_doctor",
            options={"type": hl7_data_types.HL7_XCN_ExtendedCompositeID, "repeats": True}
        ),
        make_cell_type(
            "referring_doctor",
            options={"type": hl7_data_types.HL7_XCN_ExtendedCompositeID, "repeats": True}
        ),
        make_cell_type(
            "consulting_doctor",
            options={"type": hl7_data_types.HL7_XCN_ExtendedCompositeID, "repeats": True}
        ),
        make_cell_type("hospital_service", options={"type": HL7_CodedWithException}),
        make_cell_type("temporary_location", options={"type": HL7_PersonLocation}),
        make_cell_type("preadmit_test_indicator", options={"type": HL7_CodedWithException}),
        make_cell_type("re_admission_indicator", options={"type": HL7_CodedWithException}),
        make_cell_type("admit_source", options={"type": HL7_CodedWithException}),
        make_cell_type(
            "ambulatory_status", options={"type": HL7_CodedWithException, "repeats": True}
        ),
        make_cell_type("vip_indicator", options={"type": HL7_CodedWithException}),
        make_cell_type(
            "admitting_doctor", options={
                "type": hl7_data_types.HL7_XCN_ExtendedCompositeID, "repeats": True
            }
        ),
        make_cell_type("patient_type", options={"type": HL7_CodedWithException}),
        make_cell_type("visit_number", options={"type": HL7_ExtendedCompositeId}),
        make_cell_type("financial_class", options={"type": hl7_data_types.HL7_FinancialClass}),
        make_cell_type("charge_price_indicator", options={"type": HL7_CodedWithException}),
        make_cell_type("courtesy_code", options={"type": HL7_CodedWithException}),
        make_cell_type("credit_rating", options={"type": HL7_CodedWithException}),
        make_cell_type("contract_code", options={"type": HL7_CodedWithException, "repeats": True}),
        # next field is of unimplemented type Date (DT), implement if needed
        make_cell_type("contract_effective_date", options={"repeats": True}),
        make_cell_type("contract_amount", options={"repeats": True}),
        make_cell_type("contract_period", options={"repeats": True}),
        make_cell_type("interest_code", options={"type": HL7_CodedWithException}),
        make_cell_type("transfer_to_bad_debt_code", options={"type": HL7_CodedWithException}),
        # next field is of unimplemented type Date (DT), implement if needed
        make_cell_type("transfer_to_bad_debt_date"),
        make_cell_type("bad_debt_agency_code", options={"type": HL7_CodedWithException}),
        make_cell_type("bad_debt_transfer_amount"),
        make_cell_type("bad_debt_recovery_amount"),
        make_cell_type("delete_account_indicator", options={"type": HL7_CodedWithException}),
        # next field is of unimplemented type Date (DT), implement if needed
        make_cell_type("delete_account_date"),
        make_cell_type("discharge_disposition", options={"type": HL7_CodedWithException}),
        # next field is of unimplemented type Discharge to location and date (DLD)
        make_cell_type("discharged_to_location"),
        make_cell_type("diet_type", options={"type": HL7_CodedWithException}),
        make_cell_type("servicing_facility", options={"type": HL7_CodedWithException}),
        make_cell_type("bed_status"),
        make_cell_type("account_status", options={"type": HL7_CodedWithException}),
        make_cell_type("pending_location", options={"type": HL7_PersonLocation}),
        make_cell_type("prior_temporary_location", options={"type": HL7_PersonLocation}),
        make_cell_type("admit_date", options={"type": HL7Datetime}),
        make_cell_type("discharge_date", options={"type": HL7Datetime}),

    ],
    "OBR": [
        make_cell_type("set_id"),
        make_cell_type("placer_order_number"),
        make_cell_type("filler_order_number"),
        make_cell_type("universal_service_identifier"),
        make_cell_type("priority"),
        make_cell_type("requested_datetime"),
        make_cell_type("observation_datetime", options={"type": HL7Datetime}),
    ],
    "OBX": [
        make_cell_type("set_id"),
        make_cell_type("value_type"),
        make_cell_type("observation_identifier"),
        make_cell_type("observation_sub_id"),
        make_cell_type("observation_value", options={"repeats": True}),
        make_cell_type("units"),
        make_cell_type("references_range"),
        make_cell_type("abnormal_flags"),
        make_cell_type("probability"),
        make_cell_type("nature_of_abnormal_test"),
        make_cell_type("observation_result_status"),
        make_cell_type("effective_date_of_reference_range"),
        make_cell_type("user_defined_access_checks"),
        make_cell_type("observation_datetime"),
    ],
    "IN1": [
        make_cell_type("set_id"),
        make_cell_type(
            "health_plan_id", options={"type": HL7_CodedWithException, "required": True}
        ),
        make_cell_type(
            "insurance_company_id", options={
                "type": HL7_ExtendedCompositeId, "required": True, "repeats": True
            }
        ),
        make_cell_type("insurance_company_name"),
        make_cell_type("insurance_company_address"),
        make_cell_type("insurance_co_contact_person"),
        make_cell_type("insurance_co_phone_number"),
        make_cell_type("group_number"),
        make_cell_type("group_name"),
        make_cell_type("insureds_group_emp_id"),
        make_cell_type("insureds_group_emp_name"),
        make_cell_type("plan_effective_date", options={"type": HL7Datetime}),
        make_cell_type("plan_expiration_date", options={"type": HL7Datetime}),
        make_cell_type("authorization_information"),
        make_cell_type("plan_type", options={"type": HL7_CodedWithException}),
        make_cell_type("policy_number", index=35)
        # NOTE: standard defines more fields which can be added if needed in
        # the future
    ]
}
