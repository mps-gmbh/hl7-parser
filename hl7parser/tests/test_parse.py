#! /usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from hl7parser import HL7Message, HL7Segment, HL7Delimiters
from hl7parser.hl7_data_types import HL7Datetime

import unittest


class TestEncoding(unittest.TestCase):
    """
    Test correct handling of bytestrings and unicode strings
    """

    def test_bytestring_segment(self):
        """ bytestring segment can be cast to unicode and bytestring """
        segment = HL7Segment(b"FOO|Bääbabamm")
        str(segment)
        unicode(segment)

    def test_unicode_segment(self):
        """ unicode segment can be cast to unicode and bytestring """
        segment = HL7Segment("FOO|Bääbabamm")
        str(segment)
        unicode(segment)

    def test_bytestring_message(self):
        """ bytestring message can be cast to unicode and bytestring """
        message = HL7Message(b"MSH|Dingdong the witch is dead\nFOO|Bääbabamm")
        str(message)
        unicode(message)

    def test_unicode_message(self):
        """ unicode message can be cast to unicode and bytestring """
        message = HL7Message("MSH|Dingdong the witch is dead\nFOO|Bääbabamm")
        str(message)
        unicode(message)


class TestParsing(unittest.TestCase):
    """
        Test parsing of HL7 messages
    """
    maxDiff = None

    msg_string1 = ("MSH|^~\&|ADT1|GOOD HEALTH HOSPITAL|GHH LAB, INC.|GOOD HEALTH HOSPITAL|198808181126|SECURITY|ADT^A01^ADT_A01|MSG00001|P^default|2.7|\n"
               "EVN|A01|200708181123||\n"
               "PID|1||PATID1234^5^M11^ADT1^MR^GOOD HEALTH HOSPITAL~123456789^^^USSSA^SS||EVERYMAN^ADAM^A^III||19610615|M||C^Caucasian|&HOME STREET&2^^Greensboro^NC^27401-1020^Westeros|GL|(555) 555-2004|(555)555-2004||S|| PATID12345001^2^M10^ADT1^AN^A|444333333|987654^NC|\n"
               "NK1|1|NUCLEAR^NELDA^W|SPO^SPOUSE||||NK^NEXT OF KIN\n"
               "NK1|2|ATOMIC^NELLY^W|MOTHER||||NK^NEXT OF KIN\n"
               "PV1|1|I|2000^2012^01||||004777^ATTEND^AARON^A|||SUR||||ADM|A0|\n"
               "LOL|45|hihi^blubber~hehe^blimm|dumdidum&dumdeldi^dubbel&debbel|"
               )

    msg_string2 = ("MSH|^~\&|ADT1|GOOD HEALTH HOSPITAL|GHH LAB, INC.|GOOD HEALTH HOSPITAL|198808181126|SECURITY|ADT^A01^ADT_A01|MSG00001|P|2.7|\n"
               "EVN|A01|200708181123||\n"
               "PID|1||PATID1234^5^M11^ADT1^MR^GOOD HEALTH HOSPITAL~123456789^^^USSSA^SS||EVERYMAN^ADAM^A^III||19610615|M||C|&HOME STREET&2^^Greensboro^NC^27401-1020^Westeros|GL|(555) 555-2004|(555)555-2004||S|| PATID12345001^2^M10^ADT1^AN^A|444333333|987654^NC|"
               )

    msg_mrg = ("MSH|^~\&|HNAM_PM|HNA500|AIG||20131016140148||ADT^A34|Q150084042T145948315C489644\n"
               "PID|1||3790333^^^MSH_MRN^MRN^MTSN~2175611^^^MSH_EMPI^CMRN^UPLOAD|195511^^^IID^DONOR ID^MTSN~Q3790333^^^MSQ_MRN^KMRN|EVERYMAN^ADAM^J^^^^CURRENT||19580321|M|||77 CRANFORD COURT^^NEW YORK^NY^10038^USA^HOME^^040|040|(212)555-1212^HOM\n"
               "MRG|3150123^^^MSH_MRN^MRN^MTSN|Q3150123"
               )

    successful_query_result = "\n".join((
        "MSH|^~\&|pdv|krz|myappl|9270000|201411041444||ADR^A19|0001|P|2.2",
        "MSA|AA|test234",
        "QRD|201411041444|R|I|912268|||1^RD|3248239|DEM",
        "PID|0001||3248239||Raabe^Max|Raabe|19980322|M|||Tiergartenstr. 12^^Berlin^^10785^D||0190/123456^^PH|||||||||||||D||||N",
    ))

    insuccessful_query_result = "\n".join((
        "MSH|^~\&|pdv|krz|myappl|9270000|201411041444||ADR^A19|0001|P|2.2",
        "MSA|AE|test234|2018|||2018^#WHO-FILTER enthält falschen Wert",
    ))

    def test_successful_query_status(self):
        message = HL7Message(self.successful_query_result)

        self.assertEqual(unicode(message.msa.acknowledgement_code), "AA")

    def test_unsuccessful_query_status(self):
        message = HL7Message(self.insuccessful_query_result)

        self.assertEqual(unicode(message.msa.acknowledgement_code), "AE")
        self.assertEqual(unicode(message.msa.text_message), "2018")

    def test_datetime(self):
        message = HL7Message(self.msg_string1)
        self.assertEqual(unicode(message.pid.datetime_of_birth), '19610615')
        delimiters = HL7Delimiters(*"|^~\&")
        old = "18710826"
        dt = HL7Datetime(old, delimiters)
        self.assertEqual(unicode(dt), old)
        time = "19610615132733.0065"
        dt = HL7Datetime(time, delimiters)
        self.assertEqual(unicode(dt), time)

    def test_address(self):
        message = HL7Message(self.msg_string1)
        self.assertEqual(unicode(message.pid.patient_address), '&HOME STREET&2^^Greensboro^NC^27401-1020^Westeros')


    def test_simple_segments_parse(self):
        message = HL7Message(self.msg_string1)

        pid_seg = self.msg_string1.splitlines()[2]

        self.assertEqual(unicode(message.pid), pid_seg)

    def test_multiple_segments_parse(self):
        message = HL7Message(self.msg_string1)

        lines = self.msg_string1.splitlines()

        self.assertEqual(unicode(message.nk1[0]), lines[3])
        self.assertEqual(unicode(message.nk1[1]), lines[4])

    def test_trailing_segment_fields(self):
        pid_string = "PID|1||PATID1234^5^M11^ADT1^MR^GOOD HEALTH HOSPITAL~123456789^^^USSSA^SS||EVERYMAN^ADAM^A^III||19610615|M||C|&HOME STREET&2^^Greensboro^NC^27401-1020^Westeros|GL|(555) 555-2004|(555)555-2004"
        pid = HL7Segment(pid_string)
        self.assertEqual(unicode(pid.ssn_number_patient), '')
        self.assertEqual(unicode(pid), pid_string)

    def test_len(self):
        pid_string = "PID|1||PATID1234^^M11^ADT1^MR^HOSPITAL||EVERYMAN^ADAM^A^III||||||&HOME STREET&2^^Greensboro^NC^27401-1020^Westeros|"
        pid = HL7Segment(pid_string)
        # segment length
        self.assertEqual(len(pid), 40)
        # named field set
        self.assertTrue(pid.set_id_pid)
        # named field unset
        self.assertFalse(pid.ssn_number_patient)
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

    def test_message_parse(self):
        message = HL7Message(self.msg_string1)

        # the expected delimiters
        expected_delimiters = HL7Delimiters('|', '^', '~', '\\', '&')

        self.assertEqual(unicode(expected_delimiters),
                         unicode(message.delimiters))

        # check patient data
        self.assertEqual("ADAM", unicode(message.pid.patient_name[0].given_name))
        self.assertEqual("ADAM", unicode(message.pid[4][0][1]))
        self.assertEqual("EVERYMAN", unicode(message.pid.patient_name[0].family_name))
        # unset fields should still exist as attributes
        self.assertTrue(message.pid.patient_name[0].prefix is None)
        self.assertTrue(message.pid.patient_name[0].name_representation_code is None)

        # check correct parsing of extended composite ID
        self.assertEqual(2, len(message.pid.patient_identifier_list))

        self.assertEqual("GOOD HEALTH HOSPITAL", unicode(message.pid.patient_identifier_list[0].assigning_facility))
        self.assertEqual("123456789", unicode(message.pid.patient_identifier_list[1].id_number))

        # check correct parsing of extended adress

        self.assertEqual("HOME STREET", unicode(message.pid.patient_address[0].street_address.street_name))
        self.assertEqual("Greensboro", unicode(message.pid.patient_address[0].city))
        self.assertEqual("Westeros", unicode(message.pid.patient_address[0].country))


        # check correct parsing of coded with exception

        self.assertEqual("Caucasian", unicode(message.pid.race[0].text))

        # check correct parsing of message type

        self.assertEqual("A01", unicode(message.header.message_type.trigger_event))
        self.assertEqual("ADT", unicode(message.header.message_type.message_code))

        # check correct parsing of processing type

        self.assertEqual("P", unicode(message.header.processing_id.processing_id))
        self.assertEqual("default", unicode(message.header.processing_id.processing_mode))

        # check correct parsing of version identifier

        self.assertEqual("2.7", unicode(message.header.version_id.version_id))

        def invalid_attr():
            message.foobar
        self.assertRaises(AttributeError, invalid_attr)

    def test_unknown_message_parse(self):
        message = HL7Message(self.msg_string1)

        # check parsing of unknown message
        self.assertEqual("45", unicode(message.lol[0]))
        self.assertEqual("blubber", unicode(message.lol[1][0][1]))
        self.assertEqual("blubber", unicode(message.lol[1][0][1]))
        self.assertEqual("hehe", unicode(message.lol[1][1][0]))
        self.assertEqual("dumdeldi", unicode(message.lol[2][0][1]))
        self.assertEqual("debbel", unicode(message.lol[2][1][1]))

    def test_mrg_message_parse(self):
        message = HL7Message(self.msg_mrg)
        self.assertEqual("A34", unicode(message.header.message_type.trigger_event))
        mrg = message.mrg
        self.assertTrue(mrg.prior_patient_identifier_list)
        self.assertEqual(1, len(mrg.prior_patient_identifier_list))
        self.assertTrue(mrg.prior_patient_identifier_list[0])
        self.assertEqual("3150123", unicode(mrg.prior_patient_identifier_list[0].id_number))
        self.assertEqual("Q3150123", unicode(mrg.prior_alternate_patient_id))

    def test_pv1_segment(self):
        segment = HL7Segment(
            "PV1|1|I|2000^2012^01||||004777^ATTEND^AARON^A|||SUR||||ADM|A0|"
        )

        self.assertEqual(unicode(segment.patient_class), "I")

        self.assertEqual(
            unicode(segment.assigned_patient_location.point_of_care), "2000")
        self.assertEqual(
            unicode(segment.assigned_patient_location.room), "2012")
        self.assertEqual(
            unicode(segment.assigned_patient_location.bed), "01")

        self.assertEqual(
            unicode(segment.attending_doctor[0].person_identifier), "004777")
        self.assertEqual(
            unicode(segment.attending_doctor[0].given_name), "AARON")
        self.assertEqual(
            unicode(segment.attending_doctor[0].family_name), "ATTEND")

        self.assertEqual(
            unicode(segment.attending_doctor[0].second_name), "A")

        self.assertEqual(
            unicode(segment.hospital_service), "SUR")


if __name__ == '__main__':
    unittest.main()
