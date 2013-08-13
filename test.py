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
    
    msg_string = ("MSH|^~\&|ADT1|GOOD HEALTH HOSPITAL|GHH LAB, INC.|GOOD HEALTH HOSPITAL|198808181126|SECURITY|ADT^A01^ADT_A01|MSG00001|P|2.7|\n"
               "EVN|A01|200708181123||\n"
               "PID|1||PATID1234^5^M11^ADT1^MR^GOOD HEALTH HOSPITAL~123456789^^^USSSA^SS||EVERYMAN^ADAM^A^III||19610615|M||C|2222 HOME STREET^^GREENSBORO^NC^27401-1020|GL|(555) 555-2004|(555)555-2004||S|| PATID12345001^2^M10^ADT1^AN^A|444333333|987654^NC|\n"
               "NK1|1|NUCLEAR^NELDA^W|SPO^SPOUSE||||NK^NEXT OF KIN\n"
               "PV1|1|I|2000^2012^01||||004777^ATTEND^AARON^A|||SUR||||ADM|A0|"
               )

    def test_message_parse(self):
        message = HL7Message(self.msg_string)

        # the expected delimiters
        expected_delimiters = HL7Delimiters('|', '^', '~', '\\', '&')

        self.assertEqual(unicode(expected_delimiters),
                         unicode(message.delimiters))

        # check patient data
        self.assertEqual("ADAM", unicode(message.pid.patient_name[0].given_name))
        self.assertEqual("EVERYMAN", unicode(message.pid.patient_name[0].family_name))


        # check correct parsing of extended composite ID
        self.assertEqual(2, len(message.pid.patient_identifier_list))

        self.assertEqual("GOOD HEALTH HOSPITAL", unicode(message.pid.patient_identifier_list[0].assigning_facility))
        self.assertEqual("123456789", unicode(message.pid.patient_identifier_list[1].id_number))

        #~ self.assertEqual(
        
    #~ def test_message_roundtrip(self):
        #~ message = HL7Message(self.msg_string)
#~ 
        #~ for x in message.pid.composites:
            #~ print unicode(x) + " " + repr(x)
#~ 
        #~ # replace delimiters in message object
        message.delimiters = HL7Delimiters('$', '§', '=', '?', '!')
        #~ message.delimiters.composite = '$'
        #~ message.delimiters.subcomposite = '§'
        #~ message.delimiters.field = '='
        message.delimiters.escape = '?'
        #~ message.delimiters.subsub_composite = '!'
        #~ 
        #~ msg_copy = self.msg_string
        #~ msg_copy = (msg_copy.replace('|', '$')
                        #~ .replace('^', '§')
                        #~ .replace('~', '=')
                        #~ .replace('\\', '?')
                        #~ .replace('&', '!'))
        #~ print msg_copy
#~ 
        #~ print "\n" + unicode(message)
        #~ self.assertEqual(msg_copy, unicode(message))
if __name__ == '__main__':
    unittest.main()
