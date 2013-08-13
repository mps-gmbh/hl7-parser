#! /usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from hl7 import HL7Message, HL7Delimiters

import unittest

class TestParsing(unittest.TestCase):
    """
        Test parsing of HL7 messages
    """
    maxDiff = None
    
    msg_string1 = ("MSH|^~\&|ADT1|GOOD HEALTH HOSPITAL|GHH LAB, INC.|GOOD HEALTH HOSPITAL|198808181126|SECURITY|ADT^A01^ADT_A01|MSG00001|P|2.7|\n"
               "EVN|A01|200708181123||\n"
               "PID|1||PATID1234^5^M11^ADT1^MR^GOOD HEALTH HOSPITAL~123456789^^^USSSA^SS||EVERYMAN^ADAM^A^III||19610615|M||C^Caucasian|&HOME STREET&2^^Greensboro^NC^27401-1020^Westeros|GL|(555) 555-2004|(555)555-2004||S|| PATID12345001^2^M10^ADT1^AN^A|444333333|987654^NC|\n"
               "NK1|1|NUCLEAR^NELDA^W|SPO^SPOUSE||||NK^NEXT OF KIN\n"
               "PV1|1|I|2000^2012^01||||004777^ATTEND^AARON^A|||SUR||||ADM|A0|\n"
               "LOL|45|hihi^blubber~hehe^blimm|dumdidum&dumdeldi^dubbel&debbel|"
               )

    msg_string2 = ("MSH|^~\&|ADT1|GOOD HEALTH HOSPITAL|GHH LAB, INC.|GOOD HEALTH HOSPITAL|198808181126|SECURITY|ADT^A01^ADT_A01|MSG00001|P|2.7|\n"
               "EVN|A01|200708181123||\n"
               "PID|1||PATID1234^5^M11^ADT1^MR^GOOD HEALTH HOSPITAL~123456789^^^USSSA^SS||EVERYMAN^ADAM^A^III||19610615|M||C|&HOME STREET&2^^Greensboro^NC^27401-1020^Westeros|GL|(555) 555-2004|(555)555-2004||S|| PATID12345001^2^M10^ADT1^AN^A|444333333|987654^NC|"
               )

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

    def test_unknown_message_parse(self):
        message = HL7Message(self.msg_string1)

        # check parsing of unknown message
        self.assertEqual("45", unicode(message.lol[0]))
        self.assertEqual("blubber", unicode(message.lol[1][0][1]))
        self.assertEqual("blubber", unicode(message.lol[1][0][1]))
        self.assertEqual("hehe", unicode(message.lol[1][1][0]))
        self.assertEqual("dumdeldi", unicode(message.lol[2][0][1]))
        self.assertEqual("debbel", unicode(message.lol[2][1][1]))
                
if __name__ == '__main__':
    unittest.main()
