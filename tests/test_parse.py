#! /usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import datetime
import sys
import unittest

import pytest
import six
from hl7parser import HL7Delimiters, HL7Message, HL7Segment
from hl7parser.hl7_data_types import HL7Datetime


@pytest.mark.skipif(sys.version_info.major > 2, reason="not relevant for python 3")
def test_bytestring_segment():
    """bytestring segment can be cast to unicode and bytestring"""
    segment = HL7Segment(b"FOO|Baababamm")
    str(segment)
    six.text_type(segment)


@pytest.mark.skipif(sys.version_info.major > 2, reason="not relevant for python 3")
def test_unicode_segment():
    """unicode segment can be cast to unicode and bytestring"""
    segment = HL7Segment("FOO|Baababamm")
    str(segment)
    six.text_type(segment)


@pytest.mark.skipif(sys.version_info.major > 2, reason="not relevant for python 3")
def test_bytestring_message():
    """bytestring message can be cast to unicode and bytestring"""
    message = HL7Message(b"MSH|Dingdong the witch is dead\nFOO|Baababamm")
    str(message)
    six.text_type(message)


@pytest.mark.skipif(sys.version_info.major > 2, reason="not relevant for python 3")
def test_unicode_message():
    """unicode message can be cast to unicode and bytestring"""
    message = HL7Message("MSH|Dingdong the witch is dead\nFOO|Baababamm")
    str(message)
    six.text_type(message)


class TestParsing(unittest.TestCase):
    """
    Test parsing of HL7 messages
    """

    msg_string1 = (
        "MSH|^~\&|ADT1|GOOD HEALTH HOSPITAL|GHH LAB, INC.|GOOD HEALTH HOSPITAL|198808181126|SECURITY|ADT^A01^ADT_A01|MSG00001|P^default|2.7|\n"
        "EVN|A01|200708181123||\n"
        "PID|1||PATID1234^5^M11^ADT1^MR^GOOD HEALTH HOSPITAL~123456789^^^USSSA^SS||EVERYMAN^ADAM^A^III||19610615|M||C^Caucasian|&HOME STREET&2^^Greensboro^NC^27401-1020^Westeros|GL|(555) 555-2004|(555)555-2004||S|| PATID12345001^2^M10^ADT1^AN^A|444333333|987654^NC|\n"
        "NK1|1|NUCLEAR^NELDA^W|SPO^SPOUSE||||NK^NEXT OF KIN\n"
        "NK1|2|ATOMIC^NELLY^W|MOTHER||||NK^NEXT OF KIN\n"
        "NK1|3|IVO^ISOTOPE^M|FATHER||||NK^NEXT OF KIN\n"
        "PV1|1|I|2000^2012^01||||004777^ATTEND^AARON^A|||SUR||||ADM|A0|\n"
        "LOL|45|hihi^blubber~hehe^blimm|dumdidum&dumdeldi^dubbel&debbel|"
    )

    msg_string2 = (
        "MSH|^~\&|ADT1|GOOD HEALTH HOSPITAL|GHH LAB, INC.|GOOD HEALTH HOSPITAL|198808181126|SECURITY|ADT^A01^ADT_A01|MSG00001|P|2.7|\n"
        "EVN|A01|200708181123||\n"
        "PID|1||PATID1234^5^M11^ADT1^MR^GOOD HEALTH HOSPITAL~123456789^^^USSSA^SS||EVERYMAN^ADAM^A^III||19610615|M||C|&HOME STREET&2^^Greensboro^NC^27401-1020^Westeros|GL|(555) 555-2004|(555)555-2004||S|| PATID12345001^2^M10^ADT1^AN^A|444333333|987654^NC|"
    )

    msg_mrg = (
        "MSH|^~\&|HNAM_PM|HNA500|AIG||20131016140148||ADT^A34|Q150084042T145948315C489644\n"
        "PID|1||3790333^^^MSH_MRN^MRN^MTSN~2175611^^^MSH_EMPI^CMRN^UPLOAD|195511^^^IID^DONOR ID^MTSN~Q3790333^^^MSQ_MRN^KMRN|EVERYMAN^ADAM^J^^^^CURRENT||19580321|M|||77 CRANFORD COURT^^NEW YORK^NY^10038^USA^HOME^^040|040|(212)555-1212^HOM\n"
        "MRG|3150123^^^MSH_MRN^MRN^MTSN^20131016140148^^^^|Q3150123"
    )

    successful_query_result = "\n".join(
        (
            "MSH|^~\&|pdv|krz|myappl|9270000|201411041444||ADR^A19|0001|P|2.2",
            "MSA|AA|test234",
            "QRD|201411041444|R|I|912268|||1^RD|3248239|DEM",
            "PID|0001||3248239||Raabe^Max|Raabe|19980322|M|||Tiergartenstr. 12^^Berlin^^10785^D||0190/123456^^PH|||||||||||||D||||N",
        )
    )

    insuccessful_query_result = "\n".join(
        (
            "MSH|^~\&|pdv|krz|myappl|9270000|201411041444||ADR^A19|0001|P|2.2",
            "MSA|AE|test234|2018|||2018^#WHO-FILTER enthält falschen Wert",
        )
    )

    def test_successful_query_status(self):
        message = HL7Message(self.successful_query_result)

        self.assertEqual(six.text_type(message.msa.acknowledgement_code), "AA")

    def test_unsuccessful_query_status(self):
        message = HL7Message(self.insuccessful_query_result)

        self.assertEqual(six.text_type(message.msa.acknowledgement_code), "AE")
        self.assertEqual(six.text_type(message.msa.text_message), "2018")

    def test_datetime(self):
        message = HL7Message(self.msg_string1)
        self.assertEqual(six.text_type(message.pid.datetime_of_birth), "19610615")
        delimiters = HL7Delimiters(*"|^~\&")
        old = "18710826"
        dt = HL7Datetime(old, delimiters)
        self.assertEqual(six.text_type(dt), old)
        time = "19610615132733.0065"
        dt = HL7Datetime(time, delimiters)
        self.assertEqual(six.text_type(dt), time)

    def test_address(self):
        message = HL7Message(self.msg_string1)
        self.assertEqual(
            six.text_type(message.pid.patient_address),
            "&HOME STREET&2^^Greensboro^NC^27401-1020^Westeros",
        )

    def test_simple_segments_parse(self):
        message = HL7Message(self.msg_string1)

        pid_seg = self.msg_string1.splitlines()[2]

        assert six.text_type(message.pid) == pid_seg

    def test_multiple_segments_parse(self):
        message = HL7Message(self.msg_string1)

        lines = self.msg_string1.splitlines()

        self.assertEqual(six.text_type(message.nk1[0]), lines[3])
        self.assertEqual(six.text_type(message.nk1[1]), lines[4])
        self.assertEqual(six.text_type(message.nk1[2]), lines[5])

    def test_trailing_segment_fields(self):
        pid_string = "PID|1||PATID1234^5^M11^ADT1^MR^GOOD HEALTH HOSPITAL~123456789^^^USSSA^SS||EVERYMAN^ADAM^A^III||19610615|M||C|&HOME STREET&2^^Greensboro^NC^27401-1020^Westeros|GL|(555) 555-2004|(555)555-2004|"
        pid = HL7Segment(pid_string)
        self.assertEqual(six.text_type(pid.ssn_number_patient), "")
        self.assertEqual(six.text_type(pid), pid_string)

    def test_len(self):
        pid_string = "PID|1||PATID1234^^M11^ADT1^MR^HOSPITAL||EVERYMAN^ADAM^A^III||||||&HOME STREET&2^^Greensboro^NC^27401-1020^Westeros|"
        pid = HL7Segment(pid_string)
        # segment length
        self.assertEqual(len(pid), 40)
        # named field set
        self.assertTrue(pid.set_id_pid)
        # named field unset
        self.assertFalse(pid.ssn_number_patient)
        self.assertFalse(pid.ssn_number_patient[0])
        # HL7Datetime unset
        self.assertFalse(pid.datetime_of_birth)
        # list field set
        self.assertTrue(pid.patient_identifier_list)
        # list field length
        self.assertEqual(len(pid.patient_identifier_list), 1)
        self.assertTrue(pid.patient_identifier_list[0])
        self.assertFalse(pid.patient_identifier_list[0].identifier_check_digit)

        # test unrecognized segment
        pid = HL7Segment("LOL|VALUE||^^^|")
        self.assertEqual(len(pid), 4)
        # value field set
        self.assertTrue(pid[0])
        self.assertEqual(len(pid[0]), 1)
        # value field unset
        self.assertFalse(pid[1])
        # list field set
        self.assertTrue(pid[2])
        self.assertEqual(len(pid[2]), 4)
        # list field element unset
        self.assertFalse(pid[2][0])

    def test_non_zero(self):
        pid_string = "PID|1||PATID1234||EVERYMAN^ADAM^A^III||||||&HOME STREET&2^^Greensboro^NC^27401-1020^Westeros|"
        pid = HL7Segment(pid_string)
        assert not pid.patient_id
        assert pid.patient_identifier_list[0]
        assert pid.patient_name

    def test_message_parse(self):
        message = HL7Message(self.msg_string1)

        # the expected delimiters
        expected_delimiters = HL7Delimiters("|", "^", "~", "\\", "&")

        self.assertEqual(six.text_type(expected_delimiters), str(message.delimiters))

        # check patient data
        self.assertEqual("ADAM", six.text_type(message.pid.patient_name[0].given_name))
        self.assertEqual("ADAM", six.text_type(message.pid[4][0][1]))
        self.assertEqual("EVERYMAN", six.text_type(message.pid.patient_name[0].family_name))
        # unset fields should still exist as attributes
        self.assertTrue(message.pid.patient_name[0].prefix is None)
        self.assertTrue(message.pid.patient_name[0].name_representation_code is None)

        # check correct parsing of extended composite ID
        self.assertEqual(2, len(message.pid.patient_identifier_list))

        self.assertEqual(
            "GOOD HEALTH HOSPITAL",
            six.text_type(message.pid.patient_identifier_list[0].assigning_facility),
        )
        self.assertEqual(
            "123456789", six.text_type(message.pid.patient_identifier_list[1].id_number)
        )

        # check correct parsing of extended adress

        self.assertEqual(
            "HOME STREET", six.text_type(message.pid.patient_address[0].street_address.street_name)
        )
        self.assertEqual("Greensboro", six.text_type(message.pid.patient_address[0].city))
        self.assertEqual("Westeros", six.text_type(message.pid.patient_address[0].country))

        # check correct parsing of coded with exception

        self.assertEqual("Caucasian", six.text_type(message.pid.race[0].text))

        # check correct parsing of message type

        self.assertEqual("A01", six.text_type(message.header.message_type.trigger_event))
        self.assertEqual("ADT", six.text_type(message.header.message_type.message_code))

        # check correct parsing of processing type

        self.assertEqual("P", six.text_type(message.header.processing_id.processing_id))
        self.assertEqual("default", six.text_type(message.header.processing_id.processing_mode))

        # check correct parsing of version identifier

        self.assertEqual("2.7", six.text_type(message.header.version_id.version_id))

        def invalid_attr():
            message.foobar

        self.assertRaises(AttributeError, invalid_attr)

    def test_unknown_message_parse(self):
        message = HL7Message(self.msg_string1)

        # check parsing of unknown message
        self.assertEqual("45", six.text_type(message.lol[0]))
        self.assertEqual("blubber", six.text_type(message.lol[1][0][1]))
        self.assertEqual("blubber", six.text_type(message.lol[1][0][1]))
        self.assertEqual("hehe", six.text_type(message.lol[1][1][0]))
        self.assertEqual("dumdeldi", six.text_type(message.lol[2][0][1]))
        self.assertEqual("debbel", six.text_type(message.lol[2][1][1]))

    def test_mrg_message_parse(self):
        message = HL7Message(self.msg_mrg)
        self.assertEqual("A34", six.text_type(message.header.message_type.trigger_event))
        mrg = message.mrg
        self.assertTrue(mrg.prior_patient_identifier_list)
        self.assertEqual(1, len(mrg.prior_patient_identifier_list))
        self.assertTrue(mrg.prior_patient_identifier_list[0])
        self.assertEqual("3150123", six.text_type(mrg.prior_patient_identifier_list[0].id_number))
        self.assertEqual("Q3150123", six.text_type(mrg.prior_alternate_patient_id))

    def test_pv1_segment(self):
        segment = HL7Segment(
            "PV1|1|I|2000^2012^01||123^^^^^^20190924143134&YYYYMMDDHHMMSS"
            "||004777^ATTEND^AARON^A|||SUR||||ADM|A0|"
        )

        self.assertEqual(six.text_type(segment.patient_class), "I")

        self.assertEqual(six.text_type(segment.assigned_patient_location.point_of_care), "2000")
        self.assertEqual(six.text_type(segment.assigned_patient_location.room), "2012")
        self.assertEqual(six.text_type(segment.assigned_patient_location.bed), "01")

        self.assertEqual(six.text_type(segment.attending_doctor[0].person_identifier), "004777")
        self.assertEqual(six.text_type(segment.attending_doctor[0].given_name), "AARON")
        self.assertEqual(six.text_type(segment.attending_doctor[0].family_name), "ATTEND")

        self.assertEqual(six.text_type(segment.attending_doctor[0].second_name), "A")

        self.assertEqual(six.text_type(segment.hospital_service), "SUR")

        self.assertEqual(
            six.text_type(segment.preadmit_number.effective_date.datetime), "2019-09-24 14:31:34"
        )


def test_in1_segment():
    message_data = (
        "IN1|1:1|McDH|123456789^^^^^^^^^McDonalds Health|McDonalds Health||||||"
        "||||||Musterfrau^Gertrud^^^^Dr.^L^A^|SEL|19700101|Königstr. 1B^^Stuttgart^^70173|"
        "||||||||||"
        "|||||1|12345||||||||||||||"
    )

    in1 = HL7Segment(message_data)

    assert str(in1.health_plan_id) == "McDH"
    assert str(in1.insurance_company_name) == "McDonalds Health"

    assert str(in1.policy_number) == "12345"

    name_of_insured = in1.name_of_insured
    assert str(name_of_insured) == "Musterfrau^Gertrud^^^^Dr.^L^A^"
    assert str(name_of_insured.family_name) == "Musterfrau"
    assert str(name_of_insured.given_name) == "Gertrud"
    assert str(name_of_insured.middle_name) == ""
    assert str(name_of_insured.suffix) == ""
    assert str(name_of_insured.prefix) == ""
    assert str(name_of_insured.degree) == "Dr."
    assert str(name_of_insured.name_type_code) == "L"
    assert str(name_of_insured.name_representation_code) == "A"
    assert str(name_of_insured.name_context) == ""

    assert str(in1.insureds_relationship_to_patient) == "SEL"
    assert str(in1.insureds_date_of_birth) == "19700101"

    insureds_address = in1.insureds_address
    assert str(insureds_address) == "Königstr. 1B^^Stuttgart^^70173"
    assert str(insureds_address.street_address) == "Königstr. 1B"
    assert str(insureds_address.city) == "Stuttgart"
    assert str(insureds_address.zip_or_postal_code) == "70173"
